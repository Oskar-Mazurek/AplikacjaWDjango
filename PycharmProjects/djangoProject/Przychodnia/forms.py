from django.forms import ModelForm
from .models import Customer, User
from django import forms


class CustomerForm(ModelForm):
    # Haslo = forms.CharField(widget=forms.PasswordInput)

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
