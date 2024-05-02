from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from apps.Administracion.views import starter, loginAdministracion, registerAdministracion, logoutAdministracion, pago as pagoAdministrador
from apps.Cliente.views import loginCliente, pago as pagoCliente
from django.contrib.auth import views as auth_views
app_name = 'Global'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    #auth Administracion
    path('starter/',starter.as_view(),name = 'starter'),
    path('logout/',login_required(logoutAdministracion.as_view()),name = 'logoutAdministracion'),
    path('loginAdministracion/', loginAdministracion.as_view(), name = "loginAdministracion"),
    path('registerAdministracion/', registerAdministracion.as_view(), name = "registerAdministracion"),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name="Administracion/forgotPassword.html"), name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Administracion/setPasswordEmail.html"), name='password_reset_confirm'),
    path('pagoCliente/', pagoCliente, name= 'pagoCliente'),
    path('pagoAdministrador/', pagoAdministrador, name= 'pagoAdministrador'),
] 