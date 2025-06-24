from django.contrib import admin
from .models import Usuario, PerfilEmpleador, PerfilMusico
# Register your models here.

admin.site.register(Usuario)
admin.site.register(PerfilEmpleador)
admin.site.register(PerfilMusico)