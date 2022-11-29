from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    USER_TYPES = (('ADM', 'Administrator'), ('DOC', 'Lekarz'), ('PAT', 'Pacjent'))
    userType = models.CharField(max_length=3, choices=USER_TYPES, default='PAT')
    pesel = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    telephoneNumber = models.IntegerField(verbose_name='Numer telefonu', null=False, blank=False)
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
            return "Nazwa użytkownika:" + self.user.username + " Typu: Administrator"
        if (self.userType == 'DOC'):
            specializations =self.specializationdoctor_set.all()
            myString = ""
            for spec in specializations:
                myString+=f'{spec.specializations} '
            return "Nazwa użytkownika:" + self.user.username + " Typu: Lekarz" + " " + myString
        if (self.userType == 'PAT'):
            return "Nazwa użytkownika:" + self.user.username + " Typu: Pacjent"


class Term(models.Model):
    date = models.DateTimeField()
    taken = models.BooleanField(default=False,verbose_name='Pokój')
    doctor = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.CharField(max_length=6, null=True, blank=True)
    specializationName = models.CharField(max_length=15, default="")

    def __str__(self):
        if (self.taken == 1):
            return "ID:" + str(self.pk) + " Termin: " + str(self.date + timedelta(hours=2)) + " Zajęty" + " " + str(self.specializationName)
        if (self.taken == 0):
            return "ID:" + str(self.pk) + " Termin: " + str(self.date + timedelta(hours=2)) + " Wolny" + " " + str(self.specializationName)


class Visit(models.Model):
    patient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=300, blank=True, null=True)
    term = models.OneToOneField(Term, on_delete=models.CASCADE)

    def __str__(self):
        return "ID:" + str(self.pk) + f" Pacjent: {self.patient.name} {self.patient.surname} " \
                                      f"Lekarz: {self.term.doctor.name} {self.term.doctor.surname}  " \
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
