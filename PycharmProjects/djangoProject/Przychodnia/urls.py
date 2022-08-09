from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('oPrzychodni/', views.about, name='about'),
    # path('Login/', views.login, name='login'),
    path('rejestracja/', views.register, name='register'),
    path('kontakt/', views.contact, name='contact'),
    path('profil/', views.profil, name='profil'),
    path('wykazPacjentów/', views.wykazPacjentów, name='wykazPacjentów'),
    path('wykazSpecjalistów/', views.wykazSpecjalistów, name='wykazSpecjalistów'),
]
