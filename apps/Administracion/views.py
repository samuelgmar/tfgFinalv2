from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from django.views.generic import *
from .forms import *
from .models import *
from .cart import *
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from apps.Global.models import RedSocial,Product,Order, Category, SliderImage, contactoUs
from apps.Cliente.models import UsuarioNormal
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from apps.Cliente.forms import UsuarioUpdateForm,UsuarioUpdateFormdos
from apps.Administracion.forms import ProductForm, sliderForm, politicasForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import sys, json
import re
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db.models import Count

# Create your views here.
class globalVariablesRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(Usuario, pk=request.user.pk)
        self.usuarioAdministracion = get_object_or_404(UsuarioAdminstracion, user=self.usuario)
        self.productos = Product.objects.filter(administracion=self.usuarioAdministracion)
        self.usuarios_normales = UsuarioNormal.objects.filter(administracion=self.usuarioAdministracion)
        usuariosOrders =[usuario_normal.user for usuario_normal in self.usuarios_normales]
        self.ordenes = Order.objects.filter(user__in=usuariosOrders)
        self.personalizar = get_object_or_404(LotteryAdministration, nombreAdministración=self.usuarioAdministracion)
        return super().dispatch(request, *args, **kwargs)
class AdministracionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=nombre_administracion)
        if not request.user.is_administracion or request.user.usuarioadminstracion.nombre_administracion != nombre_administracion:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página")
        return super().dispatch(request, *args, **kwargs)
    
class Administracion(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'LotoHome/indexAdmin.html'
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
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context


class phf(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'Administracion/phf.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.nombre_administracion = kwargs.get('nombre_administracion')
        self.administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        context['administracion'] = self.administracion
        context['nombreAdministracion'] = self.nombre_administracion
        if self.administracion.imagen_cabecera:
            context['imagenCabecera'] = self.administracion.imagen_cabecera
        else:
            context['imagenCabecera'] = ""
        if self.administracion.logo:
            context['imagenLogo'] = self.administracion.logo
        else:
            context['imagenLogo'] = ""
        context['form'] = LotteryAdministrationForm(instance=self.administracion)
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    
    def post(self, request, *args, **kwargs):
        form = LotteryAdministrationForm(request.POST, request.FILES)
        if form.is_valid():
            administracion = form.save(commit=False)
            nombre_administracion = kwargs.get('nombre_administracion')
            administracionAntiguo = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
            usuario_administracion = UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion)
            administracion.nombreAdministración = usuario_administracion
            if 'logo' not in request.FILES:
                administracion.logo = administracionAntiguo.logo
            if 'imagen_cabecera' not in request.FILES:
                administracion.imagen_cabecera = administracionAntiguo.imagen_cabecera
            if 'logo-clear' in request.POST:
                administracion.logo.delete()
                administracion.logo = None
            if 'imagen_cabecera-clear' in request.POST:
                administracion.imagen_cabecera.delete()
                administracion.imagen_cabecera = None
            administracion.save()
            return HttpResponseRedirect(request.path)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class admProducts(AdministracionRequiredMixin,globalVariablesRequiredMixin, ListView):
    model = Pack
    template_name = 'Administracion/admProductList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    
class admProductDetail(AdministracionRequiredMixin,globalVariablesRequiredMixin, DetailView):
    model = Pack
    template_name = 'Administracion/admProductDetail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['cartProductForm'] = CartAddProductForm()
        context['cart_product_form'] = CartAddProductForm()
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context

class admsCarritoDetail(AdministracionRequiredMixin,globalVariablesRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        cart = Cart(request)
        cart_items = cart.cart.values() # Obtener todos los elementos del carrito
        cart_details = []
        # Iterar sobre los elementos del carrito y obtener detalles de cada uno
        for item_data in cart_items:
            item_type = item_data['tipo']
            if item_type == 'Product':
                # Si el elemento es un producto, obtén el objeto Product correspondiente
                product = Product.objects.get(id=item_data['item-id'])
                cart_details.append({'tipo': item_type, 'nombre': product.nombre, 'cantidad': item_data['cantidad'], 'precio': item_data['precio'], 'id':item_data['item-id']})
            elif item_type == 'Pack':
                # Si el elemento es un paquete, obtén el objeto Pack correspondiente
                pack = Pack.objects.get(id=item_data['item-id'])
                cart_details.append({'tipo': item_type, 'nombre': pack.nombre, 'cantidad': item_data['cantidad'], 'precio': item_data['precio'], 'id':item_data['item-id']})
        
        total_price = cart.get_total_price() # Calcular el total del carrito

        if not cart_details:  # Si el carrito está vacío
            mensaje = "Tu carrito está vacío."
        else:
            mensaje = None

        return render(request, 'Administracion/admCarrito.html', {'nombre_administracion': nombre_administracion, 'cart_details': cart_details, 'total_price': total_price, 'mensaje': mensaje, 'cart':cart})
    
@method_decorator(require_POST, name='dispatch')
class admsCarritoAdd(AdministracionRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        cart = Cart(request)
        pack = get_object_or_404(Pack, id=product_id)
        cart.add(item=pack,tipo="Pack")
        return redirect('Administracion:admsCarritoDetail', nombre_administracion=nombre_administracion)

@method_decorator(require_POST, name='dispatch')
class admsCarritoRemove(AdministracionRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        cart = Cart(request)
        producto = get_object_or_404(Pack, id=product_id)
        cart.remove(producto)
        return redirect('Administracion:admsCarritoDetail', nombre_administracion=nombre_administracion)

class admsPaymentSuccess(AdministracionRequiredMixin,globalVariablesRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        cart = Cart(request)
        orderf = request.session.get('nuevaOrden', None)
        order_idf = int(orderf['orden']['order_id'])
        orderf = get_object_or_404(Order, id= order_idf)
        if 'nuevaOrden' in request.session:
            del request.session['nuevaOrden']
        cart.clear()
        nueva_orden = ""
        return render(request, "Administracion/admPaymentSuccess.html", {'nombre_administracion': nombre_administracion,
                                                                         'order': orderf,
                                                                         'user':request.user,
                                                                         'usuario': self.usuario,
                                                                         'usuarioAdministracion': self.usuarioAdministracion,
                                                                         'productos': self.productos,
                                                                         'usuarios_normales': self.usuarios_normales,
                                                                         'ordenes': self.ordenes,
                                                                         'personalizar': self.personalizar
                                                                         })

class admsFactura(AdministracionRequiredMixin,globalVariablesRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        ordern = get_object_or_404(Order, id=kwargs.get('order_id'))

        return render(request, "Administracion/factura.html", {'nombre_administracion': nombre_administracion, 'order':ordern, 'user':request.user})

class admsPaymentFailed(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'Administracion/admPaymentFailed.html'


#auth
class loginAdministracion(FormView):
    model = Usuario
    template_name = 'Administracion/login.html'
    form_class = UsuarioAdminstracionFormLogin

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_administracion:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(loginAdministracion, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(loginAdministracion, self).form_valid(form)
    
    def get_success_url(self):
        usuario = get_object_or_404(Usuario, username=self.request.user.username)
        nombre_administracion = usuario.usuarioadminstracion.nombre_administracion
        starter = self.request.user.starter
        if starter==False:
            return reverse('Global:starter')

        return reverse('Administracion:homeAdministracion', kwargs={'nombre_administracion': nombre_administracion})


@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class registerAdministracion(CreateView):
    model = Usuario
    form_class = UsuarioAdminstracionFormRegister
    template_name = 'Administracion/register.html'
    success_url = reverse_lazy('homeAdministracion')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administracion'
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_administracion:
            return HttpResponseRedirect(reverse_lazy('Global:loginAdministracion'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            logout(self.request)
            user = form.save()
            login(self.request, user)
            return redirect('Global:loginAdministracion')
        else:
            user = form.save()
            login(self.request, user)
            return redirect('Global:loginAdministracion')
        
class logoutAdministracion(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('Global:loginAdministracion')


class homeAdministracion(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'Administracion/homeadm.html'
    def dispatch(self, request, *args, **kwargs):
        nombre_administracion = kwargs.get('nombre_administracion')
        self.admin=UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion)
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        decimosBajos = Product.objects.filter(administracion=self.admin, juego__in=[Product.LOTERIA_NACIONAL_S, Product.LOTERIA_NACIONAL_J],cantidad__lt=5)
        context['decimosBajos'] = decimosBajos.exclude(nombre__in=["LNJ", "LNS"])
        context['administracion'] = self.administracion
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        totalIngresoMensual = 0
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        productos_ordenados = {}
        productos_este_año = ""
        productos_hoy = ""
        meses = {i: 0 for i in range(1, 13)}
        juegos_posibles = set([choice[0] for choice in Product.GAME_CHOICES])
        productos_hoy_array = {choice[0]: 0 for choice in Product.GAME_CHOICES}
        
        orders = Order.objects.filter(administracion=self.usuarioAdministracion)
        orders_hoy = orders.filter(fechaCreacion=datetime.now().date())
        for order in orders_hoy:
            order.total = str(order.total).replace(',','.')
        context['orders_hoy'] = orders_hoy
        for order in orders:
            productos_este_año = order.obtener_productos().filter(creado__year=datetime.now().year)
            productos_hoy = order.obtener_productos().filter(creado__date=timezone.now().date())
            productos_agrupados_hoy = productos_hoy.values('juego', 'creado__date').annotate(cantidad=Count('id')).order_by('juego', 'creado__date')
            for producto in productos_agrupados_hoy:
                juego = producto['juego']
                cantidad = producto['cantidad']
                productos_hoy_array[juego] += cantidad
            productos_agrupados = productos_este_año.values('juego', 'creado__month').annotate(cantidad=Count('id')).order_by('juego', 'creado__month')
            
            for juego in juegos_posibles:
                if juego not in productos_ordenados:
                    productos_ordenados[juego] = [0] * len(meses)

            for producto_agrupado in productos_agrupados:
                juego = producto_agrupado['juego']
                mes = producto_agrupado['creado__month'] - 1  
                cantidad = producto_agrupado['cantidad']

                productos_ordenados[juego][mes] += cantidad
        productos_hoy_lista = [productos_hoy_array[juego] for juego in productos_hoy_array]
        context['productos_vendidos_hoy'] = productos_hoy_lista
        productos_ordenados_final = []
        try:
            productos_ordenados_final = {juego: productos_ordenados[juego] for juego in juegos_posibles} 
        except:
            print()
        context['productos_ordenados_final'] = productos_ordenados_final
        productos_ordenados_final_suma = 0
        try:
            productos_ordenados_final_suma = [sum(productos_ordenados_final['Loteria Nacional Sábado']),sum(productos_ordenados_final['Loteria Nacional Jueves']),sum(productos_ordenados_final['Bonoloto']),sum(productos_ordenados_final['Quinigol']),sum(productos_ordenados_final['Eurodreams']),sum(productos_ordenados_final['Euromillón']),sum(productos_ordenados_final['El Gordo']),sum(productos_ordenados_final['Quiniela']),sum(productos_ordenados_final['Primitiva'])]
        except:
            print()
        context['productos_ordenados_final_suma'] = productos_ordenados_final_suma
        orders_this_month = Order.objects.filter(fechaCreacion__month=now.month, fechaCreacion__year=now.year, administracion=self.usuarioAdministracion)
        orders_this_week = Order.objects.filter(fechaCreacion__range=[start_of_week, end_of_week], administracion=self.usuarioAdministracion)
        for order in orders_this_month:
            totalIngresoMensual += order.total
        users = Usuario.objects.filter(last_login__date=timezone.now().date())
        usuarios_activos = UsuarioNormal.objects.filter(user__in=users, administracion=self.usuarioAdministracion)
        usuarios_registrados_hoy = UsuarioNormal.objects.filter(user__in=Usuario.objects.filter(date_joined=timezone.now().date()), administracion=self.usuarioAdministracion).count()
        context['usuarios_registrados_hoy'] = usuarios_registrados_hoy
        context['totalIngresoMensual'] = totalIngresoMensual
        context['usuarios_activos_hoy'] = usuarios_activos.count()
        context['numeroOrdersSemanal'] = orders_this_week.count()
        context['personalizar'] = self.personalizar
        return context
    

class ClientesList(globalVariablesRequiredMixin,ListView):
    model = UsuarioNormal
    template_name = 'Administracion/ClientesList.html'  
    context_object_name = 'usuarios'
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset()
        nombre_administracion = self.kwargs.get('nombre_administracion')
        search_query = self.request.GET.get('q')
        queryset = UsuarioNormal.objects.filter(administracion__nombre_administracion=nombre_administracion)
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(nombreCompleto__icontains=search_query)
            )   
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    
    

class ClientesInfo(globalVariablesRequiredMixin, FormView):
    model = Usuario
    template_name = 'Administracion/ClientInfo.html'
    form_class = UsuarioUpdateFormdos

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       form = self.form_class(instance=usuario)
       context['form'] = form
       context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
       context['usuario'] = self.usuario
       context['usuarioAdministracion'] = self.usuarioAdministracion
       context['productos'] = self.productos
       context['usuarios_normales'] = self.usuarios_normales
       context['ordenes'] = self.ordenes
       context['personalizar'] = self.personalizar
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       context['nombre'] = usuario.username
       return context
    
    def post(self, request, **kwargs):
        user = Usuario.objects.filter(pk=self.kwargs.get('pk')).first()
        usuarionormal = UsuarioNormal.objects.filter(user=user).first()
        if request.POST:
            form = self.form_class(request.POST, instance=user)
            if form.is_valid():
                if(request.FILES):
                    user.imagen = request.FILES['imagen']
                    user.save()
                form.save() 
        
        usuarionormal.nombreCompleto = user.nombre +" "+ user.apellidos
        nombre_administracion = kwargs.get('nombre_administracion')
        return render(request, self.template_name, {'form': form, 'nombre_administracion':nombre_administracion, 'usuario': self.usuario, 'nombre':user.username})


class ProfileInfo(globalVariablesRequiredMixin, FormView):
    model = Usuario
    template_name = 'Administracion/ClientInfo.html'
    form_class = UsuarioUpdateForm

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       form = self.form_class(instance=usuario)
       context['form'] = form
       context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
       context['usuario'] = self.usuario
       context['usuarioAdministracion'] = self.usuarioAdministracion
       context['productos'] = self.productos
       context['usuarios_normales'] = self.usuarios_normales
       context['ordenes'] = self.ordenes
       context['personalizar'] = self.personalizar
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       context['nombre'] = usuario.username
       return context
    
    def post(self, request, **kwargs):
        usuario = get_object_or_404(Usuario, pk=request.user.pk)
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            if(request.FILES):
                usuario.imagen = request.FILES['imagen']
                usuario.save()
            form.save() 
        
        nombre_administracion = kwargs.get('nombre_administracion')
        return render(request, self.template_name, {'form': form, 'nombre_administracion':nombre_administracion, 'usuario': usuario})


class clientesPedidos(globalVariablesRequiredMixin, ListView):
    template_name = 'Administracion/OrderListClient.html'
    model = Order
    context_object_name = 'pedidos'

    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        context['pk'] = self.kwargs.get('pk')
        usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
        context['nombre'] = usuario.username

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
        queryset = Order.objects.filter(user=usuario)
        queryset = queryset.order_by('-creado')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
            )
        return queryset
    
class clientesOrders(globalVariablesRequiredMixin, ListView):
    template_name = 'Administracion/OrderList.html'
    model = Order
    context_object_name = 'pedidos'

    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Order.objects.all()
        queryset = queryset.order_by('-creado')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
            )
        return queryset
    
    def post(self, request, *args, **kwargs):
        order_id = self.request.POST.get('id')
        pedido = get_object_or_404(Order, id=order_id)
        if pedido.validado == True:
            pedido.validado = False
        else:
            pedido.validado = True

        pedido.save()
        return redirect('Administracion:admsClientePedidos', nombre_administracion=self.nombre_administracion)


  
class decimosList(globalVariablesRequiredMixin, ListView):
    template_name = 'Administracion/DecimosList.html'
    model = Product
    context_object_name = 'decimos'

    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administracion'] = self.administracion
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        context['form'] = ProductForm()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=self.kwargs.get('nombre_administracion'))
        juegos_permitidos = ['LOTERIA_NAVIDAD_J', 'LOTERIA_NACIONAL_S']
        queryset = Product.objects.filter(
            administracion=administracion,
            juego__in=[Product.LOTERIA_NACIONAL_S, Product.LOTERIA_NACIONAL_J])
        queryset = queryset.exclude(nombre__in=["LNJ", "LNS"])
        queryset = queryset.order_by('-creado')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query)
            )
        return queryset
    
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        disponibilidad = request.POST.get('disponibilidad')
        juego = request.POST.get('juego')
        cantidad = request.POST.get('cantidad')
        categoria = get_object_or_404(Category,slug= 'loteria_nacional')
        
        nuevo_producto = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            disponibilidad=True,
            juego=juego,
            cantidad=cantidad,
            slug=nombre,
            administracion=get_object_or_404(UsuarioAdminstracion, nombre_administracion=self.kwargs.get('nombre_administracion')),
            categoria=categoria,
        )
        nuevo_producto.save()
        return redirect('Administracion:admsDecimosList', nombre_administracion=self.nombre_administracion)
        
class clientesValidarOrder(globalVariablesRequiredMixin,LoginRequiredMixin, TemplateView):
    template_name = 'Administracion/OrderListEdit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('pk')
        order = Order.objects.get(id=id)

        

        context['order'] = order
        self.nombre_administracion = UsuarioAdminstracion.objects.filter(user=self.request.user).first() 
        context['nombre_administracion'] = self.nombre_administracion
        context['usuario'] = self.usuario
        context['productos'] = order.productos
        productos = order.obtener_productos()
        todo=[]
        productosMostrar=[]
        apuequip = []
        equipos=""
        mode = ""
        variable= ""
        for producto in productos:
            productosMostrar.append(producto.id)
            productosMostrar.append(str(producto.nombre))
            productosMostrar.append(str(producto.juego))
            productosMostrar.append(str(producto.categoria))
            productosMostrar.append(json.loads(producto.descripcion))
            
            variable = json.loads(producto.descripcion)     
            try:
                mode = variable['mode']
                mode = str(mode).replace(" ","").replace("\n","")
                productosMostrar.append(mode)
            except:
                mode = ""
                productosMostrar.append(mode)

            variable = json.loads(variable['variable'])
            productosMostrar.append(variable)
            
            if producto.juego == "Quiniela":
                equipos = str(variable['equiposOrden'][0]).replace("[",'["')
                equipos = equipos.replace("]",'"]')
                equipos = equipos.replace(",",'","')
                equipos = equipos.replace('" ','"')
                equipos = eval(equipos)
                
                productosMostrar.append(equipos)
                apuestas = eval(str(variable['fullApuesta']))
                tododos = []
                apuequip = []
                if mode.__contains__("Sencilla"):
                    for i,equipo in enumerate(equipos):
                        apuequip.append(equipo)
                        for index in range(0,8):
                            try:
                                apuequip.append(str(apuestas[0][index][i][0]))
                            except:
                                apuequip.append(" ")
                        tododos.append(apuequip)
                        apuequip = []
                else:
                    for i,equipo in enumerate(equipos):
                        apuequip.append(equipo)
                        print(str(apuestas[0][0][i]))
                        apuequip.append(apuestas[0][0][i])
                        tododos.append(apuequip)
                        apuequip = []
                productosMostrar.append(tododos)
            if producto.juego == "Quinigol":
                apuestas = eval(str(variable['casillasMarcadasxPartido']))
                equipos = str(variable['orden_partidos']).replace("[",'["')
                equipos = equipos.replace("]",'"]')
                equipos = equipos.replace(",",'","')
                equipos = equipos.replace('" ','"')
                equipos = eval(equipos)
                tododos = []
                apuequip = []
                productosMostrar.append(equipos)
                for i in range(0,6):
                    apuequip.append(equipos[i]) 
                    for apu in apuestas[i]:
                        partido =  "partido"+str(i)+"_"
                        apuesta = str(apu).replace(partido,"")
                        apuesta = "-".join(apuesta)
                        apuesta = apuesta.upper()
                        apuequip.append(apuesta)
                    tododos.append(apuequip)
                    apuequip = []
                productosMostrar.append(tododos)
            productosMostrar.append(str(producto.codigovalidez))
            todo.append(productosMostrar)
            productosMostrar=[]

        context['mode'] = mode        
        context['todo']= todo
        context['equipos'] = equipos
        context['descripcion'] = json.loads(producto.descripcion)
        context['variable'] = variable
        context['producto'] = producto
        return context
    def post(self, request, **kwargs):
        if request.method == 'POST':
            id = kwargs.get('pk')
            order = Order.objects.get(id=id)
            productos = order.obtener_productos()
            for producto in productos:
                valor = "id-"+str(producto.id)
                valor = request.POST.get(valor)
                producto.codigovalidez = valor
                producto.save()
            order.validado = True
            order.save()
        return redirect('Administracion:admsClientePedidos',  nombre_administracion=self.kwargs.get('nombre_administracion'))

class sliderForm(globalVariablesRequiredMixin, FormView):
    model = SliderImage
    template_name = 'Administracion/sliderForm.html'
    form_class = sliderForm

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['usuario'] = self.usuario
       images  = SliderImage.objects.filter(nombreAdministración=get_object_or_404(UsuarioAdminstracion,nombre_administracion=self.nombre_administracion))
       context['images'] = images
   
       form = self.form_class()
       context['form'] = form
       context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
       context['usuarioAdministracion'] = self.usuarioAdministracion
       context['productos'] = self.productos
       context['usuarios_normales'] = self.usuarios_normales
       context['ordenes'] = self.ordenes
       context['personalizar'] = self.personalizar
       return context
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.nombreAdministración = get_object_or_404(UsuarioAdminstracion, nombre_administracion=self.nombre_administracion)
            form.save() 
        nombre_administracion = kwargs.get('nombre_administracion')
        return redirect('Administracion:admsSlider', nombre_administracion=nombre_administracion)

@method_decorator(login_required, name='dispatch')
class BorrarSliderView(View):
    def get(self, request, **kwargs):
        image = get_object_or_404(SliderImage, pk=self.kwargs.get('pk'))
        image.delete()
        return redirect('Administracion:admsSlider', nombre_administracion=self.kwargs.get('nombre_administracion'))
    

class ContactUsList(globalVariablesRequiredMixin, ListView):
    template_name = 'Administracion/ContactUsList.html'
    model = contactoUs
    paginate_by = 30
 
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.usuario
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        nombre_administracion = self.kwargs.get('nombre_administracion')
        queryset = contactoUs.objects.filter(nombreAdministración=UsuarioAdminstracion.objects.get(nombre_administracion=nombre_administracion)).order_by('-id')
        return queryset
    
    def post(self, request, **kwargs):
        if request.method == 'POST':
            contacto = contactoUs.objects.get(id=request.POST.get('id'))
            contacto.delete()
        return redirect('Administracion:ContactusList', nombre_administracion=self.kwargs.get('nombre_administracion'))


class starter(LoginRequiredMixin, TemplateView):
    template_name = 'Administracion/starter.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        packs = Pack.objects.first()
        self.nombre_administracion = UsuarioAdminstracion.objects.filter(user=self.request.user).first() 
        precioIva = str(packs.precio).replace(',', '')
        precioIva = Decimal(precioIva)
        precioIva = precioIva * Decimal('1.21')
        precioIva = str(precioIva).replace(',', '')
        context['pack'] = packs
        context['precioIva'] = precioIva
        context['nombre_administracion'] = self.nombre_administracion
        return context

class admsPaymentFailedStarter(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'Administracion/admPaymentFailed.html'
  
def pago(request):
    if request.method == 'POST':
        user = request.user

        order_id = request.POST.get('orderID')
        nombre_usuario = request.POST.get('nombreUsuario')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        dni = request.POST.get('dni')
        calle = request.POST.get('calle')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigoPostal')
        provincia = request.POST.get('provincia')
        imagen = request.FILES['imagen']
        paypalMail = request.POST.get('paypal')
        user.nombre = nombre
        user.apellidos = apellidos
        user.dni = dni
        user.calle = calle
        user.ciudad = ciudad
        user.cPostal = codigo_postal
        user.provincia = provincia
        user.imagen = imagen
        user.starter = True
        user.paypalMail = paypalMail
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({})

class add_decimo(LoginRequiredMixin,View):
    def post(self, request, **kwargs):
        if request.method == 'POST':
            decimo = request.POST.get('decimo')
            juego = request.POST.get('juego')
            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            fecha = request.POST.get('fecha')
            descripcion = request.POST.get('descripcion')
            producto = Product()
            producto.administracion = UsuarioAdminstracion.objects.get(nombre_administracion=self.kwargs.get('nombre_administracion'))
            producto.nombre = decimo
            if juego == "Lotería Nacional Sábado":
                producto.categoria = Category.objects.get(nombre='Lotería Nacional (S)')
                producto.juego =Product.LOTERIA_NACIONAL_S
            else:
                producto.categoria = Category.objects.get(nombre='Lotería Nacional (J)')
                producto.juego =Product.LOTERIA_NACIONAL_J
            producto.cantidad = cantidad
            producto.precio = precio
            producto.fecha_sorteo = fecha.replace("/", "-")
            producto.descripcion = descripcion
            producto.disponibilidad = True
            producto.slug = decimo+" "+juego
            producto.save()
        return redirect('Administracion:admsDecimosList', nombre_administracion=self.kwargs.get('nombre_administracion'))

@method_decorator(login_required, name='dispatch')
class BorrarDecimo(View):
    def get(self, request, **kwargs):
        decimo = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        decimo.delete()
        return redirect('Administracion:admsDecimosList', nombre_administracion=self.kwargs.get('nombre_administracion'))

class DecimoEditar(globalVariablesRequiredMixin,LoginRequiredMixin, TemplateView):
    template_name = 'Administracion/DecimosEditar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('pk')
        decimo = Product.objects.get(id=id)
        decimo.fecha_sorteo = str(decimo.fecha_sorteo).replace("-", "/")
        context['decimo'] = decimo
        self.nombre_administracion = UsuarioAdminstracion.objects.filter(user=self.request.user).first() 
        context['nombre_administracion'] = self.nombre_administracion
        context['usuario'] = self.usuario
        return context
    
    def post(self, request, **kwargs):
        if request.method == 'POST':
            decimo = request.POST.get('decimo')
            juego = request.POST.get('juego')
            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            fecha = request.POST.get('fecha')
            descripcion = request.POST.get('descripcion')
            producto = Product.objects.get(id=self.kwargs.get('pk'))
            producto.administracion = UsuarioAdminstracion.objects.get(nombre_administracion=self.kwargs.get('nombre_administracion'))
            producto.nombre = decimo
            producto.categoria = Category.objects.get(nombre='Loteria Nacional')
            if juego == "Lotería Nacional Sábado":
                producto.juego =Product.LOTERIA_NACIONAL_S
            else:
                producto.juego =Product.LOTERIA_NACIONAL_J
            producto.cantidad = cantidad
            producto.precio = precio
            producto.fecha_sorteo = fecha.replace("/", "-")
            producto.descripcion = descripcion
            producto.disponibilidad = True
            producto.slug = decimo+"_"+juego.replace(" ","_")
            producto.save()
        return redirect('Administracion:EditarDecimo',pk=self.kwargs.get('pk'),  nombre_administracion=self.kwargs.get('nombre_administracion'))
  

class politicasEditar(globalVariablesRequiredMixin,LoginRequiredMixin, TemplateView):
    template_name = 'Administracion/PoliticasEditar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.usuario
        self.nombre_administracion = kwargs.get('nombre_administracion')
        self.administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.form = politicasForm(instance=self.administracion)
        context['nombre_administracion'] = self.nombre_administracion
        context['form'] = self.form
        return context
    def post(self, request, **kwargs):
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.kwargs.get('nombre_administracion'))
        form = politicasForm(request.POST, instance=administracion)
        if form.is_valid():
            form.save()
            return redirect('Administracion:PoliticasEditar', nombre_administracion=self.kwargs.get('nombre_administracion'))
        else:
            return self.render_to_response(self.get_context_data(**kwargs))
        

class redesSociales(globalVariablesRequiredMixin,ListView):
    model = RedSocial
    template_name = 'Administracion/RedesSocialesList.html'  
    context_object_name = 'usuarios'
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset()
        nombre_administracion = self.kwargs.get('nombre_administracion')
        queryset = RedSocial.objects.filter(nombreAdministración=self.usuarioAdministracion)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        return context
    def post(self, request, **kwargs):
        if request.method == 'POST':
            redsocial = RedSocial()
            redsocial.nombreAdministración = self.usuarioAdministracion
            redsocial.nombre = request.POST.get('nombre')
            redsocial.icono = request.POST.get('icono')
            redsocial.url = request.POST.get('url')
            redsocial.save()
        return redirect('Administracion:admsRedesSociales', nombre_administracion=self.kwargs.get('nombre_administracion'))
    
class redesSocialesEditar(globalVariablesRequiredMixin, TemplateView):
    model = RedSocial
    template_name = 'Administracion/RedSocialEditar.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.nombre_administracion = kwargs.get('nombre_administracion')
        administracion_existente = UsuarioAdminstracion.objects.filter(nombre_administracion=self.nombre_administracion).exists()
        administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        self.administracion = administracion
        if not administracion_existente:
            return HttpResponseNotFound('Administración no encontrada')
        if not request.user.is_authenticated:
            return redirect('Administracion:loginAdministracion', nombre_administracion= self.nombre_administracion)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       context['redsocial'] = RedSocial.objects.get(id=self.kwargs.get('pk')) 
       context['nombre_administracion'] = self.kwargs.get('nombre_administracion')
       context['usuario'] = self.usuario
       context['usuarioAdministracion'] = self.usuarioAdministracion
       context['productos'] = self.productos
       context['usuarios_normales'] = self.usuarios_normales
       context['ordenes'] = self.ordenes
       context['personalizar'] = self.personalizar
       usuario = get_object_or_404(Usuario, id=self.kwargs.get('pk'))
       context['nombre'] = usuario.username
       return context
    
    def post(self, request, **kwargs):
        if request.method == 'POST':
            redsocial = RedSocial.objects.get(id=self.kwargs.get('pk')) 
            redsocial.nombre = request.POST.get('nombre')
            redsocial.icono = request.POST.get('icono')
            redsocial.url = request.POST.get('url')
            redsocial.save()
        return redirect('Administracion:admsRedesSociales', nombre_administracion=self.kwargs.get('nombre_administracion'))
    
@method_decorator(login_required, name='dispatch')
class BorrarRedSocial(View):
    def get(self, request, **kwargs):
        redsocial = get_object_or_404(RedSocial, id=self.kwargs.get('pk'))
        redsocial.delete()
        return redirect('Administracion:admsRedesSociales', nombre_administracion=self.kwargs.get('nombre_administracion'))

class pUbicacion(AdministracionRequiredMixin,globalVariablesRequiredMixin, TemplateView):
    template_name = 'Administracion/ubicacion.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.nombre_administracion = kwargs.get('nombre_administracion')
        self.administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=self.nombre_administracion)
        context['administracion'] = self.administracion
        context['nombreAdministracion'] = self.nombre_administracion
        if self.administracion.imagen_cabecera:
            context['imagenCabecera'] = self.administracion.imagen_cabecera
        else:
            context['imagenCabecera'] = ""
        if self.administracion.logo:
            context['imagenLogo'] = self.administracion.logo
        else:
            context['imagenLogo'] = ""
        context['form'] = LotteryAdministrationForm(instance=self.administracion)
        context['usuario'] = self.usuario
        context['usuarioAdministracion'] = self.usuarioAdministracion
        context['productos'] = self.productos
        context['usuarios_normales'] = self.usuarios_normales
        context['ordenes'] = self.ordenes
        context['personalizar'] = self.personalizar
        context['administracion'] = self.administracion
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST': 
            administracion = get_object_or_404(LotteryAdministration, nombreAdministración__nombre_administracion=kwargs.get('nombre_administracion'))
            ubi = request.POST.get('ubi')
            pattern = r'src="([^"]+)"'
            match = re.search(pattern, ubi)
            if match:
                url = match.group(1)  
                administracion.iframe = url
            else:
                print("No se encontró ninguna URL en el iframe.")
            administracion.save()
        return redirect('Administracion:admsUbicacion', nombre_administracion=self.kwargs.get('nombre_administracion'))
