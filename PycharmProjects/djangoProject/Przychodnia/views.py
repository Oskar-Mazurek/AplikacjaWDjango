from django.shortcuts import render, redirect
from .forms import Rejestracja
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
    form = Rejestracja(request.POST or None, request.FILES or None)
    if form.is_valid():
        messages.info(request, 'Pomyślnie zarejestrowano!')
        form.save()

    return render(request, 'register.html', {'form': form})


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
