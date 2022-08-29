from django import forms
from django.forms import ModelForm

from .models import Customer, SpecializationDoctor, Term


class CustomerForm(ModelForm):
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


class SpecializationDoctorForm(ModelForm):
    doctor = forms.ModelChoiceField(queryset=Customer.objects.filter(userType='DOC'), empty_label='----------')

    class Meta:
        model = SpecializationDoctor
        fields = ('doctor', 'specializations')


class TermForm(ModelForm):
    doctor = forms.ModelChoiceField(queryset=Customer.objects.filter(userType='DOC'), empty_label='----------')

    class Meta:
        model = Term
        fields = ('date', 'taken', 'doctor', 'room', 'specializationName')


class EditTermForm(ModelForm):
    class Meta:
        model = Term
        fields = ('date', 'room')
        labels = {
            'date': 'Data wizyty:',
            'room': 'Pokój odbywania wizyty:'
        }

