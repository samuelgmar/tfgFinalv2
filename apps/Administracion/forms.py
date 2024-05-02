from django import forms
from django.contrib.auth.forms import *
from apps.Global.models import Usuario, UsuarioAdminstracion, LotteryAdministration, Product, SliderImage
from django.db import transaction
from django.contrib.auth import password_validation
from .models import *
from django.forms.widgets import *
from ckeditor.widgets import CKEditorWidget

class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'rounded-0 form-control', 'placeholder': ""}  # Agrega las clases que necesites
        super().__init__(*args, **kwargs)

class CustomPasswordInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'rounded-0 form-control', 'placeholder': "", 'type': 'password'}  # Agrega las clases que necesites
        super().__init__(*args, **kwargs)

class UsuarioAdminstracionFormRegister(UserCreationForm):
    nombre_administracion = forms.CharField(max_length=400, widget=CustomTextInput())
    cif = forms.CharField(max_length=9, widget=CustomTextInput())
    password1 = forms.CharField(label='Contraseña', strip=False, widget=CustomPasswordInput(),  help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='Confirmar contraseña', widget=CustomPasswordInput(), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'email', 'telefono', 'nombre_administracion', 'cif']
        widgets = {
            'username': CustomTextInput(),
            'email': CustomTextInput(),
            'telefono': CustomTextInput(),
        }

        labels = {

        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_administracion = True
        user.is_nomalUser = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        Adminstracion = UsuarioAdminstracion.objects.create(user=user)
        Adminstracion.nombre_administracion = self.cleaned_data['nombre_administracion']
        Adminstracion.cif = self.cleaned_data['cif']
        Adminstracion.save()
        lottery_administration = LotteryAdministration.objects.create(nombreAdministración=Adminstracion)
        lottery_administration.save()
        return user

class UsuarioAdminstracionFormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioAdminstracionFormLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'rounded-0 form-control'
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password'].widget.attrs['type'] = 'password'

def widgetsAdministracion():
    return {
            'logo': ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen_cabecera': ClearableFileInput(attrs={'class': 'form-control'}),
            'color_primario': forms.TextInput(attrs={'class': 'form-control'}),
            'color_secundario': forms.TextInput(attrs={'class': 'form-control'}),
            'color_footer': forms.TextInput(attrs={'class': 'form-control'}),
            'color_body': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_apertura': forms.TimeInput(attrs={'class': 'form-control'}),
            'horario_cierre': forms.TimeInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'otros_servicios': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen_fondo': forms.FileInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'promociones': forms.Textarea(attrs={'class': 'form-control'}),
            'productos_destacados': forms.Textarea(attrs={'class': 'form-control'}),
            'testimonios': forms.Textarea(attrs={'class': 'form-control'}),
            'politicas_devolucion': forms.Textarea(attrs={'class': 'form-control'}),
            'puntos_de_venta': forms.Textarea(attrs={'class': 'form-control'}),
            'eventos_especiales': forms.Textarea(attrs={'class': 'form-control'}),
            'partners': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
            'idioma_preferido': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda_preferida': forms.TextInput(attrs={'class': 'form-control'}),
            'politicas_privacidad': forms.URLInput(attrs={'class': 'form-control'}),
            'politicas_cookies': forms.URLInput(attrs={'class': 'form-control'}),
        }

class LotteryAdministrationForm(forms.ModelForm):
    class Meta:
        model = LotteryAdministration
        fields = ['logo', 'imagen_cabecera', 'color_primario', 'color_footer', 'color_secundario', 'color_body']
        exclude = ['nombreAdministración']
        widgets = widgetsAdministracion()
        labels = {
            'color_primario': 'Color primario (fondo header)',
            'color_secundario': 'Color secundario (texto header, texto footer)',
            'color_body': 'Color body (background-color body)',
            'color_footer': 'Color footer)',
        }

class CartAddProductForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1)
    override = forms.BooleanField(required=False, initial=False)

class ProductForm(forms.ModelForm):
    GAME_CHOICES = [
        ('Loteria Nacional Jueves', 'Loteria Nacional Jueves'),
        ('Loteria Nacional Sábado', 'Loteria Nacional Sábado'),
    ]
    juego = forms.ChoiceField(choices=GAME_CHOICES)
    class Meta:
        model = Product
        fields = ['nombre', 'juego', 'fecha_sorteo', 'descripcion', 'cantidad', 'precio']
        widgets = {
            'nombre': CustomTextInput(),
            'descripcion': CustomTextInput(),
        }

class sliderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.nombreAdministración = kwargs.pop('nombreAdministración', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = SliderImage
        fields = ['image', 'caption']

class politicasForm(forms.ModelForm):
    class Meta:
        model = LotteryAdministration
        fields = [
            'politicas_privacidad_resumen_title',
            'politicas_privacidad_title',
            'politicas_cookies_title',
            'politicas_privacidad_resumen',
            'politicas_privacidad',
            'politicas_cookies']
        widgets = {
            'politicas_privacidad_resumen': CKEditorWidget(),
            'politicas_privacidad': CKEditorWidget(),
            'politicas_cookies': CKEditorWidget(),
        }