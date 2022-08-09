from django.forms import ModelForm
from .models import Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerForm(ModelForm):
    # Haslo = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Customer
        exclude = ('user', 'userType')
        labels = {
            'name': 'Imię',
            'surname': 'Nazwisko',
            'pesel': 'Pesel',
            'telephoneNumber': 'Numer telefonu',
            'street': 'Ulica',
            'city': 'Miasto',
            'zipCode': 'Kod pocztowy'
        }
        prefix = 'customerForm'
