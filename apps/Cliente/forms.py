from django.contrib.auth.forms import *
from django import forms
from apps.Global.models import Usuario, UsuarioAdminstracion, contactoUs
from django.contrib.auth import password_validation
from django.db import transaction
from apps.Cliente.models import UsuarioNormal
from django.shortcuts import get_object_or_404
import re

class UsuarioClienteFormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioClienteFormLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'rounded-0 form-control'
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password'].widget.attrs['type'] = 'password'

class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'rounded-0 form-control', 'placeholder': ""}  # Agrega las clases que necesites
        super().__init__(*args, **kwargs)

class CustomPasswordInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'rounded-0 form-control', 'placeholder': "", 'type': 'password'}  # Agrega las clases que necesites
        super().__init__(*args, **kwargs)

class UsuarioClienteFormRegister(UserCreationForm):
    nombre = forms.CharField(max_length=20, widget=CustomTextInput())
    apellidos = forms.CharField(max_length=50, widget=CustomTextInput())
    password1 = forms.CharField(label='Contraseña', strip=False, widget=CustomPasswordInput(),  help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='Confirmar contraseña', widget=CustomPasswordInput(), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username','nombre', 'apellidos', 'email', 'telefono' ]
        widgets = {
            'username': CustomTextInput(),
            'email': CustomTextInput(),
            'telefono': CustomTextInput(),
        }

        labels = {

        }

    @transaction.atomic
    def save(self, nombre_administracion ,commit=True):
        user = super().save(commit=False)
        user.is_administracion = False
        user.is_nomalUser = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        Cliente = UsuarioNormal.objects.create(user=user)
        #Cliente.nombreCompleto = user.nombre+" "+user.apellidos
        Cliente.administracion = get_object_or_404(UsuarioAdminstracion, nombre_administracion=nombre_administracion)
        Cliente.save()
        return user
    
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'paypalMail', 'nombre', 'apellidos', 'dni', 'telefono',  'calle', 'ciudad', 'provincia', 'cPostal']
        widgets = {
            'dni': CustomTextInput(),
            'email': CustomTextInput(),
            'paypalMail': CustomTextInput(),
            'telefono': CustomTextInput(),
            'ciudad': CustomTextInput(),
            'calle': CustomTextInput(),
            'cPostal': CustomTextInput(),
            'nombre': CustomTextInput(),
            'apellidos': CustomTextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_regex = re.compile(r'^.+@.+\..+$')
        if not email_regex.match(email):
            raise forms.ValidationError("El correo electrónico debe tener un formato válido (por ejemplo, usuario@dominio.com)")
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        # Expresión regular para validar el formato del DNI
        dni_regex = re.compile(r'^\d{8}-[a-zA-Z]$')
        if not dni:
            raise forms.ValidationError("Este campo es requerido")
        if not dni_regex.match(dni):
            raise forms.ValidationError("El DNI debe tener el formato correcto (XXXXXXXX-X)")
        return dni
    
    def clean_telefono(self):
        telefono = str(self.cleaned_data['telefono'])
        # Verificar si el teléfono tiene exactamente 9 dígitos
        if len(telefono) != 9 or not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener exactamente 9 números")
        return telefono

    def clean_cPostal(self):
        cPostal = str(self.cleaned_data['cPostal'])
        # Verificar si el código postal tiene exactamente 5 dígitos
        if len(cPostal) != 5 or not cPostal.isdigit():
            raise forms.ValidationError("El código postal debe contener exactamente 5 números")
        return cPostal
    
    def clean_paypalMail(self):
        paypal_mail = self.cleaned_data['paypalMail']
        # Utilizamos una expresión regular para validar el formato del correo electrónico
        email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email_regex.match(paypal_mail):
            raise forms.ValidationError("El correo electrónico asociado a PayPal debe tener un formato válido")
        return paypal_mail
    
    def clean(self):
        cleaned_data = super().clean()
        ciudad = cleaned_data.get('ciudad')
        calle = cleaned_data.get('calle')
        
        # Verificar si los campos de ciudad y calle están vacíos
        if not ciudad:
            self.add_error('ciudad', "Este campo es requerido")
        if not calle:
            self.add_error('calle', "Este campo es requerido")
        
        return cleaned_data

class UsuarioUpdateFormdos(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellidos', 'dni', 'telefono',  'calle', 'ciudad', 'provincia', 'cPostal']
        widgets = {
            'dni': CustomTextInput(),
            'email': CustomTextInput(),
            'telefono': CustomTextInput(),
            'ciudad': CustomTextInput(),
            'calle': CustomTextInput(),
            'cPostal': CustomTextInput(),
            'nombre': CustomTextInput(),
            'apellidos': CustomTextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_regex = re.compile(r'^.+@.+\..+$')
        if not email_regex.match(email):
            raise forms.ValidationError("El correo electrónico debe tener un formato válido (por ejemplo, usuario@dominio.com)")
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        
        dni_regex = re.compile(r'^\d{8}-[a-zA-Z]$')
        if not dni:
            raise forms.ValidationError("Este campo es requerido")
        if not dni_regex.match(dni):
            raise forms.ValidationError("El DNI debe tener el formato correcto (XXXXXXXX-X)")
        return dni
    
    def clean_telefono(self):
        telefono = str(self.cleaned_data['telefono'])
        # Verificar si el teléfono tiene exactamente 9 dígitos
        if len(telefono) != 9 or not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener exactamente 9 números")
        return telefono

    def clean_cPostal(self):
        cPostal = str(self.cleaned_data['cPostal'])
        # Verificar si el código postal tiene exactamente 5 dígitos
        if len(cPostal) != 5 or not cPostal.isdigit():
            raise forms.ValidationError("El código postal debe contener exactamente 5 números")
        return cPostal
    
    def clean(self):
        cleaned_data = super().clean()
        ciudad = cleaned_data.get('ciudad')
        calle = cleaned_data.get('calle')
        
        # Verificar si los campos de ciudad y calle están vacíos
        if not ciudad:
            self.add_error('ciudad', "Este campo es requerido")
        if not calle:
            self.add_error('calle', "Este campo es requerido")
        
        return cleaned_data

class UsuarioUpdateFormtres(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellidos', 'dni', 'telefono',  'calle', 'ciudad', 'provincia', 'cPostal']
        widgets = {
            'username': CustomTextInput(),
            'dni': CustomTextInput(),
            'email': CustomTextInput(),
            'telefono': CustomTextInput(),
            'ciudad': CustomTextInput(),
            'calle': CustomTextInput(),
            'cPostal': CustomTextInput(),
            'nombre': CustomTextInput(),
            'apellidos': CustomTextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_regex = re.compile(r'^.+@.+\..+$')
        if not email_regex.match(email):
            raise forms.ValidationError("El correo electrónico debe tener un formato válido (por ejemplo, usuario@dominio.com)")
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        
        dni_regex = re.compile(r'^\d{8}-[a-zA-Z]$')
        if not dni:
            raise forms.ValidationError("Este campo es requerido")
        if not dni_regex.match(dni):
            raise forms.ValidationError("El DNI debe tener el formato correcto (XXXXXXXX-X)")
        return dni
    
    def clean_telefono(self):
        telefono = str(self.cleaned_data['telefono'])
        # Verificar si el teléfono tiene exactamente 9 dígitos
        if len(telefono) != 9 or not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener exactamente 9 números")
        return telefono

    def clean_cPostal(self):
        cPostal = str(self.cleaned_data['cPostal'])
        # Verificar si el código postal tiene exactamente 5 dígitos
        if len(cPostal) != 5 or not cPostal.isdigit():
            raise forms.ValidationError("El código postal debe contener exactamente 5 números")
        return cPostal
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 5:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 5 caracteres")
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos (_)")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        ciudad = cleaned_data.get('ciudad')
        calle = cleaned_data.get('calle')
        
        # Verificar si los campos de ciudad y calle están vacíos
        if not ciudad:
            self.add_error('ciudad', "Este campo es requerido")
        if not calle:
            self.add_error('calle', "Este campo es requerido")
        
        return cleaned_data

class contactoUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.nombreAdministración = kwargs.pop('nombreAdministración', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = contactoUs
        fields = ['nombre','email', 'asunto', 'mensaje']
        widgets = {
            'nombre': CustomTextInput(),
            'email': CustomTextInput(),
            'asunto': CustomTextInput(),
            'mensaje': CustomTextInput()
        }