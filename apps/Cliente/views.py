import ast
import datetime
from decimal import ROUND_HALF_UP, Decimal
import html
import locale
import time
import unicodedata
from urllib.parse import parse_qs
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic import *
from apps.Global.models import RedSocial,cart as Carrito, SliderImage, Usuario, Order, Product, Category, UsuarioAdminstracion, LotteryAdministration, Pack
from .forms import UsuarioClienteFormLogin, UsuarioClienteFormRegister
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout, views
from .cart import Cart
import json
from django.http import *
from django.views.decorators.http import require_POST
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import sys, json
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from .forms import *
from apps.Cliente.models import UsuarioNormal
from django.contrib.auth.views import PasswordResetDoneView
import paypalrestsdk
from paypalrestsdk import Payout, ResourceNotFound
import requests
from django.db.models import Q
# Create your views here.

#PAYPAL
class PayPalClient:
    def __init__(self):
        self.client_id = "AQjCzMIsGLZhzj88QdoH4w0R4cPIkXPBgUVZXLO6yZna6vJxl6ldgNsXWfQwwGldvheFMNarFT0y4oXv"
        self.client_secret = "EIJcLHDT-el4mgL97af5un-PS_2pJoBIIRL-jp5WQdrKGE4qP6TNDJyLj5ZbSi2IUmHMa8j2hTB7TT5g"
 
        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicodedata) or isinstance(data, int)
    
    ## Obtener los detalles de la transacción
class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""   
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    return response
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    # print 'Status Code: ', response.status_code
    # print 'Status: ', response.result.status
    # print 'Order ID: ', response.result.id
    # print 'Intent: ', response.result.intent
    # print 'Links:'
    # for link in response.result.links:
    #   print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    # print 'Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
    #                    response.result.purchase_units[0].amount.value)
class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
        # print "\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
        # response.result.payer.name.given_name + " " + response.result.payer.name.surname,
        # response.result.payer.phone.phone_number.national_number)
    return response
def enviarDinero(importe, email):
    client_id = "AQjCzMIsGLZhzj88QdoH4w0R4cPIkXPBgUVZXLO6yZna6vJxl6ldgNsXWfQwwGldvheFMNarFT0y4oXv"
    client_secret = "EIJcLHDT-el4mgL97af5un-PS_2pJoBIIRL-jp5WQdrKGE4qP6TNDJyLj5ZbSi2IUmHMa8j2hTB7TT5g"
    
    auth_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, auth=(client_id, client_secret), data=data)
    access_token = response.json()['access_token']
    
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    prefix = "Payouts_2024_" 
    timestamp = str(int(time.time()))
    random_suffix = str(uuid.uuid4().int)[:6]
    sender_batch_id=prefix + timestamp + "_" + random_suffix
    data = {
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payout!",
            "email_message": "You have received a payout! Thanks for using our service!"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(importe),
                    "currency": "EUR"
                },
                "note": "Thanks for your patronage!",
                "receiver": email
            }
        ]
    }

    try:
        response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payouts', headers=headers, json=data)
        if response.status_code == 200:
            print("----------------------------------->>>>>>>>>>>>>>>>>")
            print("Payout request successful!")
        else:
            print("----------------------------------->>>>>>>>>>>>>>>>>")

            print(f"Error: {response.status_code} - {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return True
    
def pago(request):
    carrito = Carrito.objects.filter(user=request.user)
    total_price_iva_str=""
    total_price_iva=""
    total_price=""
    if carrito.count() >0:
        total_price=0
        total_price_iva=0
        for producto in carrito:
            total_price = total_price + producto.producto.precio
            cantida = producto.producto.cantidad
        tax = Decimal('0.05') + total_price
        tax = tax * Decimal('0.239')
        total_price_iva = total_price + tax
        total_price_iva = total_price_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
        total_price_iva_str = str(total_price_iva).replace(',', '.')  

    data = json.loads(request.body)
    order_id = data['orderID']
    nombre_administracion = data['nombreAdm']

    detalle = GetOrder().get_order(order_id)
    detalle_precio = float(detalle.result.purchase_units[0].amount.value)
    
    if round(float(detalle_precio), 2) == round(float(total_price_iva), 2):
        administracion=UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion)
        
        pagorealizado = enviarDinero(total_price,administracion.user.paypalMail)
        
        if pagorealizado:
            trx = CaptureOrder().capture_order(order_id, debug=True)
            estadofinal = ""
            if trx.result.status == 'COMPLETED':
                estadofinal = True
            else:
                estadofinal = False
            ordernew = Order(
                administracion = UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion),
                user = request.user,
                paypalId = trx.result.id, 
                completado = estadofinal, 
                total = trx.result.purchase_units[0].payments.captures[0].amount.value, 
                nombre= trx.result.payer.name.given_name, 
                apellidos= trx.result.payer.name.surname, 
                correoCliente= trx.result.payer.email_address, 
                calle = trx.result.purchase_units[0].shipping.address.address_line_1,
                ciudad = trx.result.purchase_units[0].shipping.address.admin_area_2,
                cPostal = trx.result.purchase_units[0].shipping.address.postal_code,
                provincia = trx.result.purchase_units[0].shipping.address.admin_area_1
            )
            ordernew.save()
            for productcarrito in carrito:
                ordernew.productos.add(get_object_or_404(Product, id=productcarrito.producto.id))


            order_data = {
                'order_id': ordernew.id,
                'user_id': ordernew.user.id,
                'paypalId': ordernew.paypalId,
                'completado': ordernew.completado,
                'total': str(ordernew.total), 
                'nombre': ordernew.nombre,
                'apellidos': ordernew.apellidos,
                'correoCliente': ordernew.correoCliente,
                'calle': ordernew.calle,
                'ciudad': ordernew.ciudad,
                'cPostal': ordernew.cPostal,
                'provincia': ordernew.provincia
            }

            request.session['nuevaOrden'] = {'orden': order_data}
            data = {
                "status": True,
            }

            for car in carrito:
                cart = Carrito.objects.get(id=car.id)
                cart.delete()

            return JsonResponse(data)
        data = {
            "mensaje": "Error =("
        }
        return JsonResponse(data)

    else:
        data = {
            "mensaje": "Error =("
        }
        return JsonResponse(data)
#all
class SorteoPostMixin:
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Cliente:loginCliente', kwargs={'nombre_administracion': kwargs.get('nombre_administracion')}))
        if request.POST.get('sorteo') == 'eurodreams':
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")

            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Eurodreams'),
                nombre=request.POST.get('sorteo'),
                juego=Product.EURODREAMS,
                slug="eurodreams",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'primitiva':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Primitiva'),
                nombre=request.POST.get('sorteo'),
                juego=Product.PRIMITIVA,
                slug="primitiva",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'elgordo':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, slug='elgordo'),
                nombre=request.POST.get('sorteo'),
                juego=Product.EL_GORDO,
                slug="elgordo",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'bonoloto':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Bonoloto'),
                nombre=request.POST.get('sorteo'),
                juego=Product.BONOLOTO,
                slug="bonoloto",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'euromillones':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Euromillones'),
                nombre=request.POST.get('sorteo'),
                juego=Product.EUROMILLON,
                slug="euromillones",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'quiniela':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Quiniela'),
                nombre=request.POST.get('sorteo'),
                juego=Product.QUINIELA,
                slug="quiniela",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        if request.POST.get('sorteo') == 'quinigol':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, nombre='Quinigol'),
                nombre=request.POST.get('sorteo'),
                juego=Product.QUINIGOL,
                slug="quinigol",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                disponibilidad=True
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        if request.POST.get('sorteo') == 'LNS':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            fecha_str = request.POST.get('fecha')
            fecha_obj = datetime.datetime.strptime(fecha_str, '%d de %B de %Y')
            fecha_formateada = fecha_obj.strftime('%Y-%m-%d')
            print(request.POST)
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, slug='LNS'),
                nombre=request.POST.get('sorteo'),
                juego=Product.LOTERIA_NACIONAL_S,
                slug="LNS",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                fecha_sorteo= fecha_formateada,
                disponibilidad=True,
                cantidad=request.POST.get('cantidad')
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            carrito.save()
            productoget = Product.objects.get(id=request.POST.get('id'))
            productoget.cantidad = productoget.cantidad - int(request.POST.get('cantidad'))
            productoget.save()
        if request.POST.get('sorteo') == 'LNJ':
            data = request.POST.get('variable', '')
            datos = {k: v for k, v in request.POST.items()}
            datos_json = json.dumps(datos)
            precio = request.POST.get('precio').replace(" ", "").replace("€", "")
            precio = re.sub(r'\.(?=[^.]*$)', ',', precio).replace(".","")
            fecha_str = request.POST.get('fecha')
            fecha_obj = datetime.datetime.strptime(fecha_str, '%d de %B de %Y')
            fecha_formateada = fecha_obj.strftime('%Y-%m-%d')
            print(request.POST)
            producto = Product.objects.create(
                administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')),
                categoria= get_object_or_404(Category, slug='LNJ'),
                nombre=request.POST.get('sorteo'),
                juego=Product.LOTERIA_NACIONAL_J,
                slug="LNJ",
                descripcion=datos_json,
                precio=float(precio.replace(",",".")),
                fecha_sorteo= fecha_formateada,
                disponibilidad=True,
                cantidad=request.POST.get('cantidad')
            )
            producto.save()
            carrito = Carrito.objects.create(user=request.user,producto=producto)
            
            carrito.save()
            productoget = Product.objects.get(id=request.POST.get('id'))
            productoget.cantidad = productoget.cantidad - 1
            productoget.save()
        return redirect('Cliente:ClienteCarritoDetail', nombre_administracion=kwargs.get('nombre_administracion'))  
    
class loteriaNacional(SorteoPostMixin,TemplateView):
    template_name = 'Cliente/loteriaNacional.html'
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        self.administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not self.administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q')
        queryset = Product.objects.all()  # Define queryset here
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query)
            )
        decimosJ = queryset.filter(
            administracion=get_object_or_404(UsuarioAdminstracion, nombre_administracion=self.administracion),
        )
        decimoS = queryset.filter(
            administracion=get_object_or_404(UsuarioAdminstracion, nombre_administracion=self.administracion),
        )
        decimosJ = decimosJ.exclude(nombre__in=["LNJ", "LNS", "eurodreams", "euromillones", "primitiva", "bonoloto", "elgordo"])
        decimoS = decimoS.exclude(nombre__in=["LNJ", "LNS", "eurodreams", "euromillones", "primitiva", "bonoloto", "elgordo"])
        context['administracion'] = self.administracion
        context['dj'] = decimosJ
        context['ds'] = decimoS
        return context

class eurodreams(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/eurodreams.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class primitiva(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/primitiva.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class elgordo(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/elgordo.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class bonoloto(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/bonoloto.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class euromillones(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/euromillones.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class quiniela(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/quiniela.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get("https://juegos.loteriasyapuestas.es/jugar/la-quiniela/apuesta")
        soup = BeautifulSoup(response.text, "html.parser")

        # Obtener nombres de partidos de la primera sección
        contenedor_nombres = soup.find("div", class_="contenedor-nombres-completos")
        if contenedor_nombres:
            nombres_partidos = contenedor_nombres.find_all("span", class_="nombre-partido-completo")
            partidos_1 = [nombre_partido.get_text(strip=True) for nombre_partido in nombres_partidos]
            # Obtener nombres de partidos de la segunda sección

            contenedor_partidos = soup.find("div", class_="partidos pleno-15")
            nombre_local = contenedor_partidos.find("p", class_="equipo").text
            nombre_visitante = contenedor_partidos.find_all("p", class_="equipo")[1].text
            partido_2 = [nombre_local, nombre_visitante]

            context['partidos_1'] = partidos_1
            context['partido_2'] = partido_2
        else:
            context['error'] = 'La sección actual esta en mantenimiento pronto estaremos de vuelta.'
        context['administracion'] = self.administracion
        return context
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    

class quinigol(SorteoPostMixin, TemplateView):
    template_name = 'Cliente/quinigol.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get("https://juegos.loteriasyapuestas.es/jugar/quinigol/apuesta")
        soup = BeautifulSoup(response.text, "html.parser")
        nombre_list_partidos_texts = [nombre.text.strip() for nombre in soup.find_all('div', class_='nombre-list-partidos')]
        context['partidos'] = nombre_list_partidos_texts
        context['administracion'] = self.administracion
        return context
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
 
class homeCliente(TemplateView):
    template_name = 'Cliente/homeCliente.html'
    form_class = contactoUsForm
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        self.usuario = Usuario.objects.get(username=UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion).user.username)
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = SliderImage.objects.filter(nombreAdministración=UsuarioAdminstracion.objects.get(nombre_administracion=kwargs.get('nombre_administracion')))
        context['slider'] = sliders
        form = self.form_class()
        context['redessociales'] = RedSocial.objects.filter(nombreAdministración = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion')))
        context['usuario'] = self.usuario
        context['form'] = form
        context['administracion'] = self.administracion
        return context
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.nombreAdministración = get_object_or_404(UsuarioAdminstracion, nombre_administracion=kwargs.get('nombre_administracion'))
            form.save() 
        nombre_administracion = kwargs.get('nombre_administracion')
        return redirect('Cliente:HomeCliente', nombre_administracion=nombre_administracion)


#auth
class loginCliente(FormView):
    model = Usuario
    template_name = 'Cliente/login.html'
    form_class = UsuarioClienteFormLogin

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if request.user.is_authenticated and request.user.is_nomalUser:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(loginCliente, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(loginCliente, self).form_valid(form)
    
    def get_success_url(self):
        nombre_administracion = self.nombre_administracion
        return reverse('Cliente:HomeCliente', kwargs={'nombre_administracion': nombre_administracion})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context

@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class registerCliente(CreateView):
    model = Usuario
    form_class = UsuarioClienteFormRegister
    template_name = 'Cliente/register.html'

    def get_success_url(self):
        return reverse_lazy('HomeCliente', kwargs={'nombre_administracion': self.nombre_administracion})
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administracion'
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if request.user.is_authenticated and request.user.is_nomalUser:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        else:
            return super().dispatch(request, self.nombre_administracion, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            logout(self.request)
            user = form.save(nombre_administracion=self.nombre_administracion)
            login(self.request, user)
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        else:
            user = form.save(nombre_administracion=self.nombre_administracion)
            login(self.request, user)
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context    

class PasswordResetCliente(views.PasswordResetView):
    template_name="Cliente/forgotPassword.html"
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if request.user.is_authenticated and request.user.is_nomalUser:
            return HttpResponseRedirect(reverse_lazy('Cliente:loginCliente', kwargs={'nombre_administracion': self.nombre_administracion}))
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data['email']  
        if email and self.is_cliente(email):  
            user = Usuario.objects.get(email = email)
            administracion = UsuarioNormal.objects.get(user = user)
            self.success_url = reverse_lazy('Cliente:password_reset_done', kwargs={'nombre_administracion': administracion.administracion})
        else:
            self.success_url = reverse_lazy('password_reset_done')
        return super().form_valid(form)
        
    def is_cliente(self, email):
        user = Usuario.objects.get(email = email)
        if user.is_nomalUser:
            return True
        return False
    
    def get_email_context(self, user, token):
        context = super().get_email_context(user, token)
        print('--------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> holita')
        context['nombre_administracion'] = self.nombre_administracion
        context['administracion'] = self.administracion 
        return context
    
class logoutCliente(View):
    def get(self, request, nombre_administracion):
        if request.user.is_authenticated:
            logout(request)
        return redirect('Cliente:loginCliente', nombre_administracion=nombre_administracion)

     
class clienteCarritoDetail(View):
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context
        
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        carrito = Carrito.objects.filter(user=request.user)
        mensaje=""
        total_price_iva_str=""
        total_price_iva=""
        total_price=""
        
        if carrito.count() >0:
            total_price=0
            total_price_iva=0
            for producto in carrito:
                total_price = total_price + producto.producto.precio
                cantida = producto.producto.cantidad
            tax = Decimal('0.05') + total_price
            tax = tax * Decimal('0.239')
            total_price_iva = total_price + tax
            total_price_iva = total_price_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
            total_price_iva_str = str(total_price_iva).replace(',', '.')  
        
        else:
            mensaje = "No ha añadido ningun producto al carrito."
        return render(request, 'Cliente/carrito.html', {'administracion':self.administracion,'nombre_administracion': nombre_administracion, 'total_price': total_price, 'total_price_iva': total_price_iva, 'total_price_iva_str': total_price_iva_str, 'mensaje': mensaje, 'cart':carrito})
    def post(self, request, *args, **kwargs):
        carrito = Carrito.objects.filter(user=request.user)
        for cart in carrito:
            if str(cart.producto.id) == request.POST.get('id'):
                producto= Product.objects.get(id=cart.producto.id)
                carrito= Carrito.objects.get(id=cart.id)
                carrito.delete()
                decimos = Product.objects.get(
                    id= json.loads(producto.descripcion)["id"]
                )
                decimos.cantidad = decimos.cantidad + int(json.loads(producto.descripcion)["cantidad"])
                decimos.save()
                producto.delete()
        return redirect('Cliente:ClienteCarritoDetail',  nombre_administracion=self.kwargs.get('nombre_administracion'))
            
class clienteCarritoInfo(TemplateView):
    template_name = 'Cliente/carritoinfo.html'
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_product = kwargs.get('pk')
        producto = Product.objects.get(id=id_product)
        variable = json.loads(producto.descripcion)
        try:
            mode = variable['mode']
            mode = str(mode).replace(" ","").replace("\n","")
        except:
            mode = ""
        try:
            variable = json.loads(variable['variable'])
        except:
            ultima_clave = list(variable.keys())[-1]
            variable = variable[ultima_clave]
        todo = []
        apuequip = []
        equipos=""
        if producto.juego == "Quiniela":
            equipos = str(variable['equiposOrden'][0]).replace("[",'["')
            equipos = equipos.replace("]",'"]')
            equipos = equipos.replace(",",'","')
            equipos = equipos.replace('" ','"')
            equipos = eval(equipos)
            apuestas = eval(str(variable['fullApuesta']))
            todo = []
            apuequip = []
            if mode.__contains__("Sencilla"):
                for i,equipo in enumerate(equipos):
                    apuequip.append(equipo)
                    for index in range(0,8):
                        try:
                            apuequip.append(str(apuestas[0][index][i][0]))
                        except:
                            apuequip.append(" ")
                    todo.append(apuequip)
                    apuequip = []
            else:
                for i,equipo in enumerate(equipos):
                    apuequip.append(equipo)
                    print(str(apuestas[0][0][i]))
                    apuequip.append(apuestas[0][0][i])
                    todo.append(apuequip)
                    apuequip = []

        if producto.juego == "Quinigol":
            apuestas = eval(str(variable['casillasMarcadasxPartido']))
            equipos = str(variable['orden_partidos']).replace("[",'["')
            equipos = equipos.replace("]",'"]')
            equipos = equipos.replace(",",'","')
            equipos = equipos.replace('" ','"')
            equipos = eval(equipos)
            for i in range(0,6):
                apuequip.append(equipos[i]) 
                for apu in apuestas[i]:
                    partido =  "partido"+str(i)+"_"
                    apuesta = str(apu).replace(partido,"")
                    apuesta = "-".join(apuesta)
                    apuesta = apuesta.upper()
                    apuequip.append(apuesta)
                todo.append(apuequip)
                apuequip = []
            

        context['mode'] = mode        
        context['todo']= todo
        context['equipos'] = equipos
        context['descripcion'] = json.loads(producto.descripcion)
        context['variable'] = variable
        context['producto'] = producto
        context['administracion'] = self.administracion
        return context




class ClientePaymentSuccess(View):
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        cart = Cart(request)
        orderf = request.session.get('nuevaOrden', None)
        order_idf = int(orderf['orden']['order_id'])
        orderf = get_object_or_404(Order, id= order_idf)
        productos = orderf.obtener_productos()

        if 'nuevaOrden' in request.session:
            del request.session['nuevaOrden']

        cart.clear()
        
        return render(request, "Cliente/ClientePaymentSuccess.html", {'administracion': self.administracion, 'nombre_administracion': nombre_administracion, 'order': orderf, 'orderProducts': productos, 'user':request.user})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context
    
class ClienteFactura(View):
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        ordern = get_object_or_404(Order, id=kwargs.get('order_id'))
        productos = ordern.obtener_productos()
        return render(request, "Cliente/factura.html", {'administracion': self.administracion, 'orderProducts': productos, 'nombre_administracion': nombre_administracion, 'order':ordern, 'user':request.user})

    
class ClientePaymentFailed(TemplateView):
    template_name = 'Cliente/ClientePaymentFailed.html'
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        return context

class ClienteOrderList(ListView):
    template_name = 'Cliente/ClienteOrderList.html'
    model = Order
    context_object_name = 'pedidos'
    def dispatch(self, request, *args, **kwargs):
        self.ordenes_usuario = Order.objects.filter(user=request.user)
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['orders'] = self.ordenes_usuario.order_by('-creado')
        context['nombre_administracion'] = self.nombre_administracion
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.ordenes_usuario.order_by('-creado')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(creado__icontains=search_query)
            )
        return queryset
    
class UsuarioUpdateView(FormView):
    model = Usuario
    template_name = 'Cliente/profile.html'
    form_class = UsuarioUpdateFormtres

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(Usuario, pk=request.user.pk)
        self.ordenes_usuario = Order.objects.filter(user=request.user)
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, **kwargs):
        usuario = get_object_or_404(Usuario, pk=request.user.pk)
        usuarionormal = get_object_or_404(UsuarioNormal, user=usuario)
        form = self.form_class(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save() 
        usuario = get_object_or_404(Usuario, pk=request.user.pk)
        usuarionormal = get_object_or_404(UsuarioNormal, user=usuario)
        usuarionormal.nombreCompleto = usuario.nombre +" "+ usuario.apellidos
        nombre_administracion = kwargs.get('nombre_administracion')
        return redirect('Cliente:profile', nombre_administracion= self.nombre_administracion)

    def get_context_data(self, **kwargs):
        usuario = get_object_or_404(Usuario, pk=self.request.user.pk)
        form = self.form_class(instance=self.usuario)
        context = super().get_context_data(**kwargs)
        context['usuario'] = usuario
        context['form'] = form
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context
    
class politica(TemplateView):
    template_name = 'Cliente/pp.html'
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.administracion.politicas_privacidad_resumen)
        context['administracion'] = self.administracion
        return context
    
class resultados(TemplateView):
    template_name = 'Cliente/resultados.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = "https://www.loteriasyapuestas.es/es/resultados"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            div_ultimos_resultados = soup.find("div", class_="r-ultimos-resultados")
            if div_ultimos_resultados:
                for img in div_ultimos_resultados.find_all("img"):
                    if img.find_parents(class_="c-ultimo-resultado__desplegable--millon"):
                        img["src"] = "https://www.loteriasyapuestas.es/f/loterias/estaticos/imagenes/sass/LogoMillon.svg"
                    elif img.find_parents(class_="c-ultimo-resultado__joker-posicion"):
                        img["src"] = "https://www.loteriasyapuestas.es/f/loterias/estaticos/imagenes/sass/LogoJoker.svg"
                    else:
                        img.extract()
                for a_tag in div_ultimos_resultados.find_all("a", title="Otros resultados"):
                    a_tag.extract()
                for a_tag in div_ultimos_resultados.find_all("a", class_="c-ultimo-resultado__otros-resultados--lototurf"):
                    a_tag.extract()
                for a_tag in div_ultimos_resultados.find_all("div", id="qa_ultResult-LOTU"):
                    a_tag.extract()
                for a_tag in div_ultimos_resultados.find_all("p", class_="c-ultimo-resultado__mas-info"):
                    a_tag.extract()
                for a_tag in div_ultimos_resultados.find_all("p", class_="c-resultado-sorteo__mas-info"):
                    a_tag.extract()    
                for a_tag in div_ultimos_resultados.find_all("p", text="Ver por orden de aparición"):
                    a_tag.extract()                 
                updated_html = div_ultimos_resultados.prettify()
                
                context['resultadosSorteo'] = updated_html
        else:
            print("No se pudo obtener el contenido de la página.")
        context['administracion'] = self.administracion
        return context
    
class estadisticas(TemplateView):
    template_name = 'Cliente/estadisticas.html'
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        #if not request.user.is_authenticated:
        #    return redirect('Cliente:loginCliente', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = "https://lotestats.com/"

        
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser").prettify
        context['statsSorteo'] = soup

        # Agregar otros datos al contexto si es necesario
        context['administracion'] = self.administracion

        return context
    
class CustomPasswordResetDoneView(TemplateView):
    template_name="Cliente/passwordResetConfirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.nombre_administracion
        return context
