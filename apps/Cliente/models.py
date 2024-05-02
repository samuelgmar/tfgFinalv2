from django.db import models
from django.urls import reverse
from apps.Global.models import Usuario
from apps.Global.models import UsuarioAdminstracion
# Create your models here.
class UsuarioNormal(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    administracion =  models.ForeignKey(UsuarioAdminstracion, on_delete=models.SET_NULL, null=True)
    nombreCompleto = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['nombreCompleto']

    class Meta:
        verbose_name = 'Usuario (cliente)'
        verbose_name_plural = 'Usuarios (clientes)'

    def __str__(self):
        return self.user.username