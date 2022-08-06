from django.contrib import admin
from .models import Customer, Term, Visit, Specialization, SpecializationDoctor

# Register your models here.
admin.site.register(Customer)
# admin.site.register(Pacjenci)
# admin.site.register(Lekarze)
# admin.site.register(Administratorzy)
admin.site.register(Visit)
admin.site.register(Term)
admin.site.register(Specialization)
admin.site.register(SpecializationDoctor)
