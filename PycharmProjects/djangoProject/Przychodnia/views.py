from django.shortcuts import render, redirect

from . import forms
from .forms import CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html',
                      {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
    else:
        userForm = UserCreationForm(request.POST)
        customerForm = CustomerForm(request.POST)
        # if userForm.is_valid() and customerForm.is_valid():
        checkUser = request.POST['username']
        #coś nie zgadza się w if, is_valid jest chyba powodem
        if request.POST['password1'] == request.POST['password2'] and userForm.is_valid() and customerForm.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                            request.POST['password1'])  # tutaj brakuje porównania z bazą danych
            messages.info(request, 'Pomyślnie zarejestrowano! Teraz zaloguj się')  # komunikat ze success
            user.save()
        else:
            messages.info(request, 'Błąd w formularzu!')  # komunikat z bledem
        return render(request, 'registration/register.html',
                      {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
    # login(request, user)
    # return redirect('homepage')  # komunikat ze success


# else:
# return render(request, 'registration/register.html',
# {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
# zwrocil  return render(request, 'registration/register.html', {'customerForm': CustomerForm(), 'userForm':UserCreationForm()})
# komunikat z bledem


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
