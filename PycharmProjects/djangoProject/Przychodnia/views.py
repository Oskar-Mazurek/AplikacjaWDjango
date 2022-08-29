import random
from datetime import date

import environ
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from twilio.rest import Client

from .forms import CustomerForm, EditProfileForm, EditTermForm
from .models import *
from .tokens import account_verification_token

env = environ.Env()
environ.Env.read_env()


# Create your views here.
def homepage(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


# logowanie
def log(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'authenticationForm': AuthenticationForm(), })
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, 'Udało się zalogować')
            return redirect('homepage')
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Nie udało się zalogować, błędne dane logowania')
            return render(request, 'registration/login.html', {'authenticationForm': AuthenticationForm(), })


@login_required
def logoutUser(request):
    logout(request)
    messages.error(request, 'Wylogowano')
    return redirect('homepage')


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html',
                      {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
    else:

        customerForm = CustomerForm(request.POST)

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password1'])
            except IntegrityError:
                messages.error(request,
                               'Spróbuj ponownie. Podany użytkownik istnieje już w bazie, popraw formularz rejestracji')
                return render(request, 'registration/register.html',
                              {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
            messages.success(request, 'Pomyślnie zarejestrowano! Teraz zaloguj się')  # komunikat ze success
            user.is_active = False
            user.save()
            currentSite = get_current_site(request)
            mailSubject = 'Potwierdzenie adresu email'
            message = render_to_string('accountActivationEmail.html', {'user': user,
                                                                       'domain': currentSite.domain,
                                                                       'uid': urlsafe_base64_encode(
                                                                           force_bytes(user.pk)),
                                                                       'token': account_verification_token.make_token(
                                                                           user)})
            email = EmailMessage(mailSubject, message, to=[user.email])
            email.send()
            if customerForm.is_valid():
                customer = customerForm.save(commit=False)
                customer.user = user
                customer.save()
                # return redirect login
                redirect('homepage')
            else:
                messages.error(request, 'Błąd w formularzu!')  # komunikat z bledem
                return render(request, 'registration/register.html',
                              {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
        else:
            messages.error(request, 'Błąd w formularzu!')  # komunikat z bledem
            return render(request, 'registration/register.html',
                          {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
    return render(request, 'registration/register.html',
                  {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})


def contact(request):
    return render(request, 'contact.html')


def getVisitSpecName(visits):
    for visit in visits:
        term = visit.term
        visitSpec = term.specializationName
        visit.specializationName = visitSpec


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    customer = get_object_or_404(Customer, user=user)
    today = date.today()
    visits = Visit.objects.filter(patient=customer, term__date__gte=today).order_by('term__date')
    getVisitSpecName(visits)

    return render(request, 'profile.html', {'user': user, 'customer': customer, 'visits': visits})


@login_required
def patientsList(request):
    reqUserType = get_object_or_404(Customer, user=request.user, userType='DOC')
    if reqUserType:
        patients = Customer.objects.filter(userType='PAT').order_by('surname')
        return render(request, 'patientsList.html',
                      {'patients': patients})


@login_required
def doctorsList(request):
    specializations = Specialization.objects.all().order_by('name')
    return render(request, 'doctorsList.html', {'specializations': specializations})


# data, specjalizacje, imie, nazwisko, pokoj
@login_required
def showAvailableTerms(request, specialization):
    spec = get_object_or_404(Specialization, name=specialization)
    specDoctors = SpecializationDoctor.objects.filter(specializations=spec)
    today = date.today()
    for specDoctor in specDoctors:
        specTerms = Term.objects.filter(taken=False, doctor=specDoctor.doctor, date__gte=today,
                                        specializationName=specialization).order_by('date')
        try:
            terms = terms | specTerms
        except:
            terms = specTerms
    # terms = Term.objects.filter(taken=False, date__gte=today).order_by('date')
    # lista = queryset1 | queryset2
    return render(request, 'showAvailableTerms.html', {'terms': terms, 'specialization': specialization})


def makeVisit(request, termId):
    if request.method == 'GET':
        return render(request, 'makeVisit.html', {'termId': termId})

    else:
        pat = get_object_or_404(Customer, user=request.user)
        purpose = request.POST['purpose']
        term = get_object_or_404(Term, pk=termId)
        visit = Visit.objects.create(patient=pat, purpose=purpose, term=term)
        visit.save()
        term.taken = True
        term.save()
        messages.success(request, 'Utworzono wizytę')
        return redirect('profile')


@login_required
def changePassword(request):
    if request.method == 'GET':
        passwordChangeForm = PasswordChangeForm(request.user)
    else:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            user = passwordChangeForm.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Twoje hasło zostało zmienione!')
            return redirect('changePassword')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')
    return render(request, 'changePassword.html', {'form': passwordChangeForm})


@login_required
def editProfile(request):
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'GET':
        editProfileForm = EditProfileForm(instance=customer)
    else:
        editProfileForm = EditProfileForm(instance=customer, data=request.POST)
        if editProfileForm.is_valid():
            editProfileForm.save()
            messages.success(request, 'Twoje dane zostały zmienione!')
            return redirect('editProfile')
        else:
            messages.error(request, 'Popraw błędy w formularzu!')
    return render(request, ' editProfile.html', {'form': editProfileForm})


def cancelVisit(request, visitId):
    visit = get_object_or_404(Visit, pk=visitId)
    userTelephoneNumber = request.user.customer.telephoneNumber
    termID = visit.term.pk
    term = get_object_or_404(Term, pk=termID)
    visitSpec = term.specializationName
    visit.specializationName = visitSpec
    # SMS preparation

    # account_sid = env('TWILIO_ACCOUNT_SID')
    # auth_token = env('TWILIO_AUTH_TOKEN')
    # MyTwilioPhoneNumber = env('MyTwilioPhoneNumber')
    # client = Client(account_sid, auth_token)

    # verificationCode = ""
    # for i in range(6):
    #     index = random.randrange(10)
    #     verificationCode += str(index)
    # print(verificationCode)

    if request.method == 'POST':

        # message = client.messages.create(
        #     body=f'Twój kod weryfikacyjny do odwołania wizyty:{verificationCode}',
        #     from_=MyTwilioPhoneNumber,
        #     to=f'+48{userTelephoneNumber}'
        # )
        # print("request.POST["+request.POST['verificationCode'])
        # if request.POST['verificationCode'] == verificationCode:
        term.taken = False
        term.save()
        visit.delete()
        messages.success(request, 'Usunięto wizytę' + str(visitId))
        return redirect('profile')
        # else:
        #     messages.error(request, 'Wpisany kod jest nie poprawny')

    return render(request, 'cancelVisit.html', {'visit': visit})


@login_required()
def doctorProfile(request):
    user = get_object_or_404(User, pk=request.user.id)
    doctor = get_object_or_404(Customer, user=user, userType='DOC')
    today = date.today()
    terms = Term.objects.filter(doctor=doctor, date__gte=today, taken=True).order_by('date')
    visitsList = []
    for term in terms:
        visit = term.visit
        visit.specName = term.specializationName
        visitsList.append(visit)

    return render(request, 'doctorProfile.html', {'user': user, 'doctor': doctor, 'visits': visitsList})


def editVisitByDoctor(request, visitId):
    visit = get_object_or_404(Visit, pk=visitId)
    term = visit.term
    editTermForm = EditTermForm(request.POST or None, instance=term)

    if editTermForm.is_valid():
        editTermForm.save()
        messages.success(request, 'Edycja wizyty:' + str(visitId) + " udana")
        return redirect('doctorProfile')

    return render(request, 'editVisitByDoctor.html', {'editTermForm': editTermForm, 'visitId': visitId})


def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
    if account_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Potwierdzono adres email')
        return redirect('profile')
    else:
        messages.success(request, 'Błąd potwierdzenia adresu email')
        return redirect('homepage')
