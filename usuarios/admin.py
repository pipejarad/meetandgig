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

# Admin para catálogos normalizados
@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'portafolios_count')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria')
    ordering = ('categoria', 'nombre')
    
    def portafolios_count(self, obj):
        return obj.portafolioinstrumento_set.count()
    portafolios_count.short_description = 'Portafolios'
    portafolios_count.admin_order_field = 'portafolioinstrumento__count'


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta', 'portafolios_count')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'
    
    def portafolios_count(self, obj):
        return obj.portafoliogenero_set.count()
    portafolios_count.short_description = 'Portafolios'


@admin.register(NivelExperiencia)
class NivelExperienciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'años_rango', 'orden')
    list_filter = ('orden',)
    ordering = ('orden',)
    
    def años_rango(self, obj):
        if obj.años_maximos:
            return f"{obj.años_minimos}-{obj.años_maximos} años"
        return f"{obj.años_minimos}+ años"
    años_rango.short_description = 'Rango años'


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region', 'pais', 'activo', 'portafolios_count')
    list_filter = ('region', 'pais', 'activo')
    search_fields = ('nombre', 'region')
    ordering = ('orden', 'region', 'nombre')
    
    def portafolios_count(self, obj):
        return obj.portafolio_set.count()
    portafolios_count.short_description = 'Portafolios'

# Registrar modelos adicionales
admin.site.register(PortafolioInstrumento)
admin.site.register(PortafolioGenero)
admin.site.register(Multimedia)
admin.site.register(Testimonio)
