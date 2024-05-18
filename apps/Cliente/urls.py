from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
app_name = 'Cliente'
urlpatterns = [
    path('', homeCliente.as_view(), name='HomeCliente'),
    path('loteriaNacional/', loteriaNacional.as_view(), name='loteriaNacional'),
    path('eurodreams/', eurodreams.as_view(), name='eurodreams'),
    path('primitiva/', primitiva.as_view(), name='primitiva'),
    path('elgordo/', elgordo.as_view(), name='elgordo'),
    path('bonoloto/', bonoloto.as_view(), name='bonoloto'),
    path('euromillones/', euromillones.as_view(), name='euromillones'),
    path('quiniela/', quiniela.as_view(), name='quiniela'),
    path('quinigol/', quinigol.as_view(), name='quinigol'),
    #auth Cliente
    path('loginCliente/', loginCliente.as_view(), name = "loginCliente"),
    path('logoutCliente/', logoutCliente.as_view(), name = "logoutCliente"),
    path('registerCliente/', registerCliente.as_view(), name = "registerCliente"),
    path('forgot_password/', PasswordResetCliente.as_view(), name='forgotPasswordCliente'),
    path('forgot_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Cliente/setPasswordEmail.html"), name='password_reset_confirm'),
    path('forgot_password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="Cliente/resetPasswordComplete.html"), name='password_reset_complete'),
    path('profile/', UsuarioUpdateView.as_view(), name='profile'),
    #pago
    path('carrito/', clienteCarritoDetail.as_view(), name = "ClienteCarritoDetail"),
    path('carrito/<int:pk>/', clienteCarritoInfo.as_view(), name = "ClienteCarritoInfo"),
    path('ClienteOrderList/<int:pk>/', ClienteOrderListInfo.as_view(), name = "ClienteOrderListInfo"),
    path('privacy-policy/', politica.as_view(), name = "privacyPolicy"),
    path('ClienteOrderList/', ClienteOrderList.as_view(), name = "ClienteOrderList"),
    path('PaymentFailed/', ClientePaymentFailed.as_view(), name = "ClientePaymentFailed"),
    path('PaymentSuccess/', ClientePaymentSuccess.as_view(), name = "ClientePaymentSuccess"),
    
    path('ClienteFactura/<int:order_id>/', ClienteFactura.as_view(), name = "ClienteFactura"),
    path('estadisticas/', estadisticas.as_view(), name = "estadisticas"),
    path('resultados/', resultados.as_view(), name = "resultados"),
    
] 
