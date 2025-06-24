from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    tipo_usuario = models.CharField(max_length=10, choices=[("musico", "Músico"), ("empleador", "Empleador")])
    foto_perfil = models.ImageField(upload_to="fotos_perfil/", null=True, blank=True)

    

class PerfilMusico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    instrumento_principal = models.CharField(max_length=100)
    estilo_musical = models.CharField(max_length=100)
    bio = models.TextField()
    experiencia_años = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=100)
    portafolio_url = models.URLField(blank=True)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username


class PerfilEmpleador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_organizacion = models.CharField(max_length=100)
    tipo_entidad = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    contacto_alternativo = models.CharField(max_length=100, blank=True)