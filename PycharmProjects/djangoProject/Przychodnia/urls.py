from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('oPrzychodni/', views.about, name='Przychodnia-about'),
    # path('Login/', views.login, name='Przychodnia-login'),
    path('rejestracja/', views.register, name='register'),
    path('Kontakt/', views.contact, name='Przychodnia-contact'),
    path('Profil/', views.profil, name='Przychodnia-profil'),
    path('WykazPacjentów/', views.wykazPacjentów, name='Przychodnia-wykazPacjentów'),
    path('WykazSpecjalistów/', views.wykazSpecjalistów, name='Przychodnia-wykazSpecjalistów'),
]
