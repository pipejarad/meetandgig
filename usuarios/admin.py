from django.contrib import admin
from .models import (
    Usuario, PerfilEmpleador, PerfilMusico, Portafolio, 
    Instrumento, Genero, NivelExperiencia, Ubicacion,
    PortafolioInstrumento, PortafolioGenero, Multimedia, Testimonio
)


class PerfilMusicoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'telefono', 'fecha_nacimiento', 
        'recibir_notificaciones_email', 'mostrar_telefono_publico'
    )
    list_filter = (
        'recibir_notificaciones_email', 'mostrar_telefono_publico'
    )
    search_fields = ('usuario__username', 'usuario__email', 'telefono', 'direccion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario',)
        }),
        ('Datos Personales', {
            'fields': ('telefono', 'fecha_nacimiento', 'direccion', 'contacto_emergencia')
        }),
        ('Configuraciones de Privacidad', {
            'fields': ('recibir_notificaciones_email', 'mostrar_telefono_publico')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )


# Inline admin para instrumentos del portafolio
class PortafolioInstrumentoInline(admin.TabularInline):
    model = PortafolioInstrumento
    extra = 1
    fields = ('instrumento', 'es_principal', 'nivel_dominio', 'años_experiencia', 'orden_presentacion')


# Inline admin para géneros del portafolio
class PortafolioGeneroInline(admin.TabularInline):
    model = PortafolioGenero
    extra = 1
    fields = ('genero', 'preferencia', 'años_experiencia', 'orden_presentacion')


# Inline admin para multimedia del portafolio
class MultimediaInline(admin.TabularInline):
    model = Multimedia
    extra = 1
    fields = ('titulo', 'tipo', 'archivo', 'url_externa', 'es_principal', 'orden')


# Inline admin para testimonios del portafolio
class TestimonioInline(admin.TabularInline):
    model = Testimonio
    extra = 1
    fields = ('nombre_cliente', 'empresa_evento', 'testimonio', 'puntuacion', 'verificado')


class PortafolioAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'slug', 'nivel_experiencia', 'ubicacion', 
        'disponible_para_gigs', 'activo', 'fecha_creacion'
    )
    list_filter = (
        'nivel_experiencia', 'ubicacion', 'disponible_para_gigs', 
        'activo', 'show_email', 'show_social_links'
    )
    search_fields = ('usuario__username', 'usuario__email', 'slug', 'biografia')
    readonly_fields = ('slug', 'fecha_creacion', 'fecha_actualizacion')
    prepopulated_fields = {}
    
    inlines = [PortafolioInstrumentoInline, PortafolioGeneroInline, MultimediaInline, TestimonioInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'slug', 'biografia')
        }),
        ('Experiencia y Formación', {
            'fields': ('nivel_experiencia', 'años_experiencia', 'formacion_musical', 'ubicacion')
        }),
        ('Enlaces y Redes Sociales', {
            'fields': (
                'website_personal', 'soundcloud_url', 'youtube_url', 
                'spotify_url', 'instagram_url', 'facebook_url', 'video_demo'
            ),
            'classes': ('collapse',)
        }),
        ('Información Comercial', {
            'fields': ('disponible_para_gigs', 'tarifa_base')
        }),
        ('Configuraciones de Visibilidad', {
            'fields': (
                'show_email', 'show_social_links', 'show_education', 
                'show_tarifa', 'show_telefono'
            ),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'activo'),
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
admin.site.register(Portafolio, PortafolioAdmin)

# Registrar catálogos  
admin.site.register(Instrumento)
admin.site.register(Genero)
admin.site.register(NivelExperiencia)
admin.site.register(Ubicacion)

# Registrar modelos adicionales
admin.site.register(PortafolioInstrumento)
admin.site.register(PortafolioGenero)
admin.site.register(Multimedia)
admin.site.register(Testimonio)
