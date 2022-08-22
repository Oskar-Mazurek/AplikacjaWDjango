from django.contrib import admin

from .forms import SpecializationDoctorForm, TermForm
from .models import Customer, Term, Visit, Specialization, SpecializationDoctor

# Register your models here.
admin.site.register(Customer)
admin.site.register(Visit)


class TermAdmin(admin.ModelAdmin):
    form = TermForm


admin.site.register(Term, TermAdmin)
admin.site.register(Specialization)


class SpecDocAdmin(admin.ModelAdmin):
    form = SpecializationDoctorForm


admin.site.register(SpecializationDoctor, SpecDocAdmin)
