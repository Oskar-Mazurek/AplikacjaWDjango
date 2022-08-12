from django.shortcuts import render, redirect
from django.db import IntegrityError
from . import forms
from .forms import CustomerForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def homepage(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


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
def profil(request):
    return render(request, 'profil.html')


@login_required
def wykazPacjentów(request):
    pacjenci = Customer.objects.filter(userType='PAT')
    return render(request, 'wykazPacjentów.html',
                  {'pacjenci': pacjenci})


@login_required
def wykazSpecjalistów(request):
    specjaliści = Customer.objects.filter(userType='DOC')
    # specjalizacja = LekarzSpecjalizacja.objects.all()
    # s=Specjalizacje.objects.select_related('IdSpecjalizacji')
    return render(request, 'wykazSpecjalistów.html',
                  {'specjaliści': specjaliści, })

# 'specjalizacja': specjalizacja
