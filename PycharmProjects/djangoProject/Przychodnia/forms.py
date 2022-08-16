from django import forms
from django.forms import ModelForm

from .models import Customer


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


class EditProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('telephoneNumber', 'street', 'city', 'zipCode')
        labels = {
            'telephoneNumber': 'Numer telefonu',
            'street': 'Ulica',
            'city': 'Miasto',
            'zipCode': 'Kod pocztowy'
        }
