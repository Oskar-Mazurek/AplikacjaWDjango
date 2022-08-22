from django.contrib import admin

from .forms import SpecializationDoctorForm
from .models import Customer, Term, Visit, Specialization, SpecializationDoctor

# Register your models here.
admin.site.register(Customer)
admin.site.register(Visit)
admin.site.register(Term)
admin.site.register(Specialization)


class SpecDocAdmin(admin.ModelAdmin):
    form = SpecializationDoctorForm


admin.site.register(SpecializationDoctor, SpecDocAdmin)
