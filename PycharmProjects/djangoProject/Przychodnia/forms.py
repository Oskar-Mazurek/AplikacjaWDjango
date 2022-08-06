from django.forms import ModelForm
from .models import Customer, User
from django import forms


class Rejestracja(ModelForm):
    # Haslo = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['user', 'userType', 'name', 'surname', 'pesel', 'telephoneNumber', 'street', 'city',
                  'zipCode']
        labels = {
            'userType': 'Typ użytkownika',
            'name': 'Imię',
            'surname': 'Nazwisko',
            'pesel': 'Pesel',
            'telephoneNumber': 'Numer telefonu',
            'street': 'Ulica',
            'city': 'Miasto',
            'zipCode': 'Kod pocztowy'
        }
