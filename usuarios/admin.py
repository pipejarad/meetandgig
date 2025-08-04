from django.contrib import admin
from .models import Usuario, PerfilEmpleador, PerfilMusico


class PerfilMusicoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'instrumento_principal', 'ubicacion', 
        'nivel_experiencia', 'disponible_para_gigs', 'perfil_publico'
    )
    list_filter = (
        'instrumento_principal', 'nivel_experiencia', 
        'disponible_para_gigs', 'perfil_publico'
    )
    search_fields = ('usuario__username', 'usuario__email', 'ubicacion', 'generos_musicales')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario',)
        }),
        ('Información Básica', {
            'fields': ('biografia', 'ubicacion', 'foto_portada')
        }),
        ('Instrumentos y Géneros', {
            'fields': ('instrumento_principal', 'instrumentos_secundarios', 'generos_musicales')
        }),
        ('Experiencia y Formación', {
            'fields': ('nivel_experiencia', 'años_experiencia', 'formacion_musical')
        }),
        ('Enlaces y Redes Sociales', {
            'fields': (
                'website_personal', 'soundcloud_url', 'youtube_url', 
                'spotify_url', 'instagram_url', 'facebook_url'
            ),
            'classes': ('collapse',)
        }),
        ('Información Profesional', {
            'fields': (
                'disponible_para_gigs', 'tarifa_base', 'video_demo', 
                'perfil_publico'
            )
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )


class PerfilEmpleadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_organizacion', 'tipo_entidad', 'ubicacion')
    search_fields = ('usuario__username', 'nombre_organizacion', 'tipo_entidad')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario',)
        }),
        ('Información de la Organización', {
            'fields': (
                'nombre_organizacion', 'tipo_entidad', 
                'ubicacion', 'contacto_alternativo'
            )
        })
    )


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_active', 'date_joined')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PerfilEmpleador, PerfilEmpleadorAdmin)
admin.site.register(PerfilMusico, PerfilMusicoAdmin)
