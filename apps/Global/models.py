from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from decimal import Decimal, ROUND_DOWN
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField

# Create your models here.
class BaseUsuarioManager(BaseUserManager):
    def _create_user(self, username, email, telefono, password, is_active, is_staff, is_administracion, is_nomalUser, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            telefono=telefono,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_administracion=is_administracion,
            is_nomalUser=is_nomalUser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, telefono, is_staff, password=None, **extra_fields):
        return self._create_user(username, email, telefono, password, is_staff, False, False, False, **extra_fields)
    
    def create_superuser(self, username, email, telefono, password=None, **extra_fields):
        return self._create_user(username, email, telefono ,password=password,is_active=True, is_staff=True, is_superuser=True, is_administracion=False, is_nomalUser=False, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    PROVINCIAS_ESPANA = [
        ('AL', 'Almería'),
        ('CA', 'Cádiz'),
        ('CO', 'Córdoba'),
        ('GR', 'Granada'),
        ('HU', 'Huelva'),
        ('JA', 'Jaén'),
        ('MA', 'Málaga'),
        ('SE', 'Sevilla'),
        ('AB', 'Albacete'),
        ('CR', 'Ciudad Real'),
        ('CU', 'Cuenca'),
        ('GU', 'Guadalajara'),
        ('TO', 'Toledo'),
        ('AV', 'Ávila'),
        ('BU', 'Burgos'),
        ('LE', 'León'),
        ('P', 'Palencia'),
        ('SA', 'Salamanca'),
        ('SG', 'Segovia'),
        ('SO', 'Soria'),
        ('VA', 'Valladolid'),
        ('ZA', 'Zamora'),
        ('HU', 'Huesca'),
        ('TE', 'Teruel'),
        ('Z', 'Zaragoza'),
        ('O', 'Asturias'),
        ('C', 'Cantabria'),
        ('VI', 'Álava'),
        ('BI', 'Bizkaia'),
        ('SS', 'Gipuzkoa'),
        ('C', 'A Coruña'),
        ('LU', 'Lugo'),
        ('OU', 'Ourense'),
        ('PO', 'Pontevedra'),
        ('BA', 'Badajoz'),
        ('CC', 'Cáceres'),
        ('TF', 'Santa Cruz de Tenerife'),
        ('GC', 'Las Palmas'),
        ('CE', 'Ceuta'),
        ('ML', 'Melilla'),
        ('MU', 'Murcia'),  
        ('MD', 'Madrid'),  
        ('LO', 'La Rioja'),  
        ('H', 'Huesca'), 
        ('AS', 'Asturias'), 
        ('S', 'Cantabria'),  
        ('ZA', 'Zaragoza'),  
        ('NA', 'Navarra'),  
        ('PV', 'País Vasco')  
    ]

    email = models.EmailField('Email', max_length=254,unique=True)
    paypalMail = models.EmailField('paypalMail', max_length=254, null = True, blank=True)
    username = models.CharField('Usuario',max_length=100, unique=True)
    dni = models.CharField('DNI',max_length=50, blank = True, null = True)
    calle = models.CharField('Calle',max_length=50, blank = True, null = True, default='')
    ciudad = models.CharField('Ciudad',max_length=50, blank = True, null = True)
    cPostal = models.CharField('Código Postal',max_length=50, blank = True, null = True)
    provincia = models.CharField('Provincia', max_length=10, choices=PROVINCIAS_ESPANA, blank = True, null = True)
    nombre = models.CharField('Nombre', max_length=200, blank = True, null = True)
    apellidos = models.CharField('Apellidos', max_length=200,blank = True, null = True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200,blank = True,null = True)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_administracion = models.BooleanField(default=False)
    starter = models.BooleanField(default=False)
    is_nomalUser = models.BooleanField(default=False)
    telefono = models.IntegerField('Telefono (+34)',unique=True, blank = True, null = True)
    objects = BaseUsuarioManager()
    date_joined = models.DateField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'telefono']

    def __str__(self):
        return f'{self.username}'
    
    def get_nombre_provincia(self):
        for codigo_prov, nombre_prov in Usuario.PROVINCIAS_ESPANA:
            if codigo_prov == self.provincia:
                return nombre_prov
        return None
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True



class Category(models.Model):
    nombre = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre

class Pack(models.Model):
    nombre = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True)
    descripcion = models.TextField(blank=True)
    descripcion_larga = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('nombre',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('admsProductsDetail', args=[self.id, self.slug])

class UsuarioAdminstracion(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nombre_administracion = models.CharField('Administracion', unique = True, max_length=400)
    cif = models.CharField('CIF', unique = True, max_length=9)
    REQUIRED_FIELDS = ['nombre_administracion', 'cif']
    pack = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = 'Administración'
        verbose_name_plural = 'Administraciones'

    def __str__(self):
        return self.nombre_administracion
    

 
class Product(models.Model):
    LOTERIA_NACIONAL_J = 'Loteria Nacional Jueves'
    LOTERIA_NACIONAL_S = 'Loteria Nacional Sábado'
    LOTERIA_NACIONAL = 'Loteria Nacional'
    LOTERIA_NINO = 'Loteria Niño'
    LOTERIA_NAVIDAD = 'Loteria Navidad'
    QUINIGOL = 'Quinigol'
    QUINIELA = 'Quiniela'
    BONOLOTO = 'Bonoloto'
    EUROMILLON = 'Euromillón'
    EURODREAMS = 'Eurodreams'
    PRIMITIVA = 'Primitiva'
    EL_GORDO = 'El Gordo'
    
    GAME_CHOICES = [
        (LOTERIA_NACIONAL_S, 'Lotería Nacional Sábado'),
        (LOTERIA_NACIONAL_J, 'Lotería Nacional Jueves'),
        (LOTERIA_NACIONAL, 'Lotería Nacional'),
        (LOTERIA_NINO, 'Loteria Niño'),
        (LOTERIA_NAVIDAD, 'Loteria Navidad'),
        (QUINIGOL, 'Quinigol'),
        (QUINIELA, 'Quiniela'),
        (BONOLOTO, 'Bonoloto'),
        (EUROMILLON, 'Euromillón'),
        (EURODREAMS, 'Eurodreams'),
        (PRIMITIVA, 'Primitiva'),
        (EL_GORDO, 'El Gordo'),
    ]
    administracion = models.ForeignKey(UsuarioAdminstracion, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Category, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, db_index=True)
    juego = models.CharField(max_length=50, choices=GAME_CHOICES)
    slug = models.SlugField(max_length=200, db_index=True)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True)
    fecha_sorteo = models.DateField(verbose_name='Fecha del Sorteo', blank=True, null=True)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    codigovalidez = models.CharField(blank=True,max_length=200)
    actualizado = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('nombre',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.nombre
    def idp(self):
        return self.id
    def get_absolute_url(self):
        return reverse('admsProductsDetail', args=[self.id, self.slug])


    
class Order(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    administracion = models.ForeignKey(UsuarioAdminstracion, on_delete=models.CASCADE)
    paypalId = models.CharField(max_length=200, blank=True, null=True)
    productos = models.ManyToManyField(Product, blank=True)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    completado = models.BooleanField(default=False)
    correoCliente = models.EmailField('Email', max_length=254, blank=True, null=True)
    calle = models.CharField('Calle',max_length=50, blank = True, null = True, default='')
    ciudad = models.CharField('Ciudad',max_length=50, blank = True, null = True)
    cPostal = models.CharField('Código Postal',max_length=50, blank = True, null = True)
    provincia = models.CharField('Provincia', max_length=10, blank = True, null = True)
    nombre = models.CharField('Nombres', max_length=200, blank = True, null = True)
    apellidos = models.CharField('Apellidos', max_length=200,blank = True, null = True)
    validado = models.BooleanField(default=False)
    fechaCreacion = models.DateField(auto_now_add=True, blank = True)
    def __str__(self):
        return f'Order {self.id} - {self.user.username}'
    
    def calcular_total(self):
        total = 0
        for producto in self.productos.all():
            total += producto.precio
        if self.pack:   
            total += self.pack.precio
        return total
    
    def calcular_total_productos(self):
        total_productos = sum(producto.precio for producto in self.productos.all())
        return total_productos

    def calcular_total_pack(self):
        total_pack = self.pack.precio if self.pack else 0
        return total_pack
    
    def total_con_iva(self):
        total_sin_iva = self.calcular_total()
        total_con_iva = total_sin_iva * Decimal('1.21')  # Añadir 21% de IVA
        total_con_iva = total_con_iva.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return total_con_iva
    
    def obtener_productos(self):
        return self.productos.all()
    
def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.nombreAdministración.user.id, filename)

class SliderImage(models.Model):
    nombreAdministración = models.ForeignKey(UsuarioAdminstracion, on_delete=models.CASCADE, null=True, related_name='sliders')
    image = models.ImageField(upload_to=user_directory_path)
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption if self.caption else "Slider Image"


class LotteryAdministration(models.Model):
    nombreAdministración = models.OneToOneField(UsuarioAdminstracion, on_delete=models.CASCADE, primary_key=True)
    logo = models.ImageField(upload_to=user_directory_path,default='LotoFinder/static/imgs/logo.png', blank=True)
    imagen_cabecera = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    color_primario = models.CharField(max_length=7, default='#ffffff', null=False)
    color_footer = models.CharField(max_length=7, default='#000000', null=False)
    color_secundario = models.CharField(max_length=7, default='#000000', null=False)
    color_body = models.CharField(max_length=7, default='#fffff', null=False)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    horario_apertura = models.TimeField(null=True, blank=True)
    horario_cierre = models.TimeField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    redes_sociales = models.JSONField(null=True, blank=True)  # Puedes ajustar según la estructura necesaria
    sitio_web = models.URLField(null=True, blank=True)
    otros_servicios = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    imagen_fondo = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    slogan = models.CharField(max_length=200, null=True, blank=True)
    promociones = models.TextField(null=True, blank=True)
    productos_destacados = models.TextField(null=True, blank=True)
    testimonios = models.TextField(null=True, blank=True)
    politicas_devolucion = models.TextField(null=True, blank=True)
    puntos_de_venta = models.TextField(null=True, blank=True)
    eventos_especiales = models.TextField(null=True, blank=True)
    partners = models.TextField(null=True, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    rating = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    idioma_preferido = models.CharField(max_length=50, null=True, blank=True)
    moneda_preferida = models.CharField(max_length=50, null=True, blank=True)
    politicas_privacidad_resumen_title = models.TextField(null=True, blank=True)
    politicas_privacidad_title = models.TextField(null=True, blank=True)
    politicas_cookies_title = models.TextField(null=True, blank=True)
    politicas_privacidad_resumen = RichTextField(null=True, blank=True)
    politicas_privacidad = RichTextField(null=True, blank=True)
    politicas_cookies = RichTextField(null=True, blank=True)
    iframe = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.nombreAdministración.nombre_administracion
    

class contactoUs(models.Model):
    nombreAdministración = models.ForeignKey(UsuarioAdminstracion, on_delete=models.CASCADE, null=True, related_name='contactUs')
    nombre = models.TextField(null=True, blank=True, max_length=100)
    email = models.EmailField('Email', max_length=254, blank=True, null=True)
    asunto = models.TextField(null=True, blank=True, max_length=200)
    mensaje = models.TextField(null=True, blank=True)

class cart(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

class RedSocial(models.Model):
    nombreAdministración = models.ForeignKey(UsuarioAdminstracion, on_delete=models.CASCADE, null=True, related_name='redsocial')
    nombre = models.CharField(max_length=100)
    url = models.URLField()
    icono = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
