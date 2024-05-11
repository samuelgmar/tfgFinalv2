from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .views import *
app_name = 'Administracion'
urlpatterns = [
    path('', login_required(homeAdministracion.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "homeAdministracion"),
    
    
    path('productos/', login_required(admProducts.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsProducts"),
    path('productos/<pk>/', login_required(admProductDetail.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsProductsDetail"),
    path('carrito/', login_required(admsCarritoDetail.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsCarritoDetail"),
    path('add/<int:product_id>/', login_required(admsCarritoAdd.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsCarritoAdd"),
    path('remove/<int:product_id>/', login_required(admsCarritoRemove.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsCarritoRemove"),
    path('PaymentSuccess/', login_required(admsPaymentSuccess.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsPaymentSuccess"),
    path('PaymentFailed/', login_required(admsPaymentFailed.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsPaymentFailed"),
    path('PaymentFailedStarter/', login_required(admsPaymentFailedStarter.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsPaymentFailedStarter"),
    path('factura/<int:order_id>/', login_required(admsFactura.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsFactura"),
    path('clientesPedidos/<int:pk>/', login_required(clientesPedidos.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsClientesPedidos"),
    path('clientesPedidos/', login_required(clientesOrders.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsClientePedidos"),
    path('clientesPedidos/order-<int:pk>/', login_required(clientesValidarOrder.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "clientesValidarOrder"),
    
    path('clientesInfo/<int:pk>/', login_required(ClientesInfo.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsClientesInfo"),
    path('clientesList/', login_required(ClientesList.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsClientesList"),
    path('ContactList/', login_required(ContactUsList.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "ContactusList"),
    path('borrarSlider/<int:pk>/', login_required(BorrarSliderView.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "borrarSlider"),
    path('añadirDecimo/', login_required(add_decimo.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "añadirDecimo"),
    path('p-hf/', login_required(phf.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsP-hf"),
    path('slider/', login_required(sliderForm.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsSlider"),
    path('profileInfo/<int:pk>/', login_required(ProfileInfo.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsProfileInfo"),
    path('decimosList/', login_required(decimosList.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsDecimosList"),
    path('borrarDecimo/<int:pk>/', login_required(BorrarDecimo.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "BorrarDecimo"),
    path('EditarDecimo/<int:pk>/', login_required(DecimoEditar.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "EditarDecimo"),
    path('EditarPoliticas/', login_required(politicasEditar.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "PoliticasEditar"),
    path('redesSociales/', login_required(redesSociales.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsRedesSociales"),
    path('borrarRedesSociales/<int:pk>/', login_required(BorrarRedSocial.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsRedesSocialesBorrar"),
    path('redesSocialesEditar/<int:pk>/', login_required(redesSocialesEditar.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsRedesSocialesEditar"),
    path('ubi/', login_required(pUbicacion.as_view(), login_url=reverse_lazy('Global:loginAdministracion')), name = "admsUbicacion"),

]
