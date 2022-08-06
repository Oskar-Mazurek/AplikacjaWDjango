from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='Przychodnia-home'),
    path('oPrzychodni/', views.about, name='Przychodnia-about'),
    # path('Login/', views.login, name='Przychodnia-login'),
    path('Rejestracja/', views.register, name='Przychodnia-register'),
    path('Kontakt/', views.contact, name='Przychodnia-contact'),
    path('Profil/', views.profil, name='Przychodnia-profil'),
    path('WykazPacjentów/', views.wykazPacjentów, name='Przychodnia-wykazPacjentów'),
    path('WykazSpecjalistów/', views.wykazSpecjalistów, name='Przychodnia-wykazSpecjalistów'),
]
