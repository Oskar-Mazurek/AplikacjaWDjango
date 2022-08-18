from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('oPrzychodni/', views.about, name='about'),
    path('kontakt/', views.contact, name='contact'),
    path('profil/', views.profile, name='profile'),
    path('wykazPacjentow/', views.patientsList, name='patientsList'),
    path('wykazSpecjalistow/', views.doctorsList, name='doctorsList'),
    # auth
    path('login/', views.log, name='login'),
    path('rejestracja/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('zmianaHasla/', views.changePassword, name='changePassword'),
    path('edycjaProfilu/', views.editProfile, name='editProfile'),
]
# tak robi się klasowo
# path('password_reset', PasswordResetView.as_view(), name='password_reset'),
# path('password_reset_done', PasswordResetDoneView.as_view(), name='password_reset_done'),
# path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
# path('password_reset_complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
