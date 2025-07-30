from django.contrib import admin
from .models import Usuario, PerfilEmpleador, PerfilMusico


class PerfilMusicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'instrumento_principal',
                    'estilo_musical', 'disponibilidad')


class PerfilEmpleadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_organizacion', 'tipo_entidad')
    search_fields = ('usuario__username', 'nombre_organizacion', 'tipo_entidad')

# Register your models here.


admin.site.register(Usuario)
admin.site.register(PerfilEmpleador)
admin.site.register(PerfilMusico)
