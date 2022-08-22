from datetime import date

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomerForm, EditProfileForm
from .models import *


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
            user.save()
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


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    customer = get_object_or_404(Customer, user=user)
    today = date.today()
    visits = Visit.objects.filter(patient=customer, term__date__gte=today).order_by('term__date')
    # specDoctors = SpecializationDoctor.objects.filter() brakuje specjalizacji
    return render(request, 'profile.html', {'user': user, 'customer': customer, 'visits': visits})


@login_required
def patientsList(request):
    reqUserType = get_object_or_404(Customer, user=request.user, userType='DOC')
    if reqUserType:
        patients = Customer.objects.filter(userType='PAT')
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
        specTerms = Term.objects.filter(taken=False, doctor=specDoctor.doctor, date__gte=today).order_by('date')
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
    termID = visit.term.pk
    term = get_object_or_404(Term, pk=termID)
    doctorID = term.doctor.pk
    doctor = get_object_or_404(Customer, pk=doctorID)
    # specDoc = get_object_or_404(SpecializationDoctor, doctor=doctor)
    # jak wypisać specjalizację lekarza dla określonej wizyty
    if request.method == 'POST':
        term.taken = False
        term.save()
        visit.delete()
        messages.success(request, 'Usunięto wizytę' + str(visitId))
        return redirect('profile')
    return render(request, 'cancelVisit.html', {'visit': visit})
    # return render(request, 'cancelVisit.html', {'visit': visit, 'specDoc': specDoc})
