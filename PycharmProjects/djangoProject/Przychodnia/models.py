from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    USER_TYPES = (('ADM', 'Administrator'), ('DOC', 'Lekarz'), ('PAT', 'Pacjent'))
    userType = models.CharField(max_length=3, choices=USER_TYPES, default='PAT')
    pesel = models.IntegerField(unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    telephoneNumber = models.IntegerField(blank=True)
    street = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    zipCode = models.CharField(max_length=6)

    def displayUserType(self):
        if (self.userType == 'ADM'):
            return "Administrator"
        if (self.userType == 'DOC'):
            return "Lekarz"
        if (self.userType == 'PAT'):
            return "Pacjent"

    def __str__(self):
        if (self.userType == 'ADM'):
            return "Nazwa użytkownika:" + str(self.user.username) + " Typu: Administrator"
        if (self.userType == 'DOC'):
            return "Nazwa użytkownika:" + str(self.user.username) + " Typu: Lekarz"
        if (self.userType == 'PAT'):
            return "Nazwa użytkownika:" + str(self.user.username) + " Typu: Pacjent"


class Term(models.Model):
    date = models.DateTimeField()
    taken = models.BooleanField(default=False)
    doctor = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        if (self.taken == 1):
            return "Termin: " + str(self.date) + " Zajęty"
        if (self.taken == 0):
            return "Termin: " + str(self.date) + " Wolny"


class Visit(models.Model):
    patient = models.OneToOneField(Customer, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=300, blank=True, null=True)
    term = models.OneToOneField(Term, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pacjent: {self.patient.name} {self.patient.surname} " \
               f"Lekarz: {self.term.doctor.name} {self.term.doctor.surname} " \
               f"Data: {self.term.date}"


class Specialization(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class SpecializationDoctor(models.Model):
    doctor = models.ForeignKey(Customer, on_delete=models.CASCADE)
    specializations = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return f'Lekarz: {self.doctor.name} {self.doctor.surname} ' \
               f'Specjalizacje: {self.specializations.name}'
