from django.contrib import admin
from .models import (
    Usuario, PerfilEmpleador, PerfilMusico, Portafolio, 
    Instrumento, Genero, NivelExperiencia, Ubicacion,
    PortafolioInstrumento, PortafolioGenero, Multimedia, Testimonio,
    OfertaLaboral, Postulacion, OfertaInstrumento, OfertaGenero
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


# ADMIN PARA OFERTAS LABORALES (Sprint 3)
class OfertaInstrumentoInline(admin.TabularInline):
    model = OfertaInstrumento
    extra = 1
    fields = ('instrumento', 'es_obligatorio', 'prioridad')


class OfertaGeneroInline(admin.TabularInline):
    model = OfertaGenero
    extra = 1
    fields = ('genero', 'prioridad')


@admin.register(OfertaLaboral)
class OfertaLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'empleador', 'estado', 'ubicacion', 'nivel_experiencia_minimo',
        'cupos_disponibles', 'fecha_publicacion', 'fecha_limite_postulacion'
    )
    list_filter = (
        'estado', 'tipo_contrato', 'ubicacion__region', 
        'nivel_experiencia_minimo', 'fecha_creacion'
    )
    search_fields = (
        'titulo', 'descripcion', 'empleador__nombre_organizacion',
        'empleador__usuario__username', 'empleador__usuario__email'
    )
    readonly_fields = ('slug', 'fecha_creacion', 'fecha_actualizacion', 'fecha_publicacion')
    inlines = [OfertaInstrumentoInline, OfertaGeneroInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('empleador', 'titulo', 'slug', 'descripcion', 'requisitos')
        }),
        ('Detalles Laborales', {
            'fields': (
                'tipo_contrato', 'fecha_evento', 'duracion_estimada',
                'cupos_disponibles', 'fecha_limite_postulacion'
            )
        }),
        ('Ubicación y Experiencia', {
            'fields': ('ubicacion', 'nivel_experiencia_minimo')
        }),
        ('Presupuesto', {
            'fields': ('presupuesto_minimo', 'presupuesto_maximo', 'presupuesto_a_convenir')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'fecha_publicacion'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'empleador__usuario', 'ubicacion', 'nivel_experiencia_minimo'
        )


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = (
        'musico', 'oferta_laboral', 'tipo_postulacion', 'estado',
        'fecha_postulacion', 'fecha_respuesta'
    )
    list_filter = (
        'tipo_postulacion', 'estado', 'fecha_postulacion',
        'oferta_laboral__empleador__nombre_organizacion'
    )
    search_fields = (
        'musico__username', 'musico__email', 'oferta_laboral__titulo',
        'portafolio__usuario__username'
    )
    readonly_fields = ('fecha_postulacion', 'fecha_respuesta')
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('oferta_laboral', 'musico', 'portafolio')
        }),
        ('Tipo y Estado', {
            'fields': ('tipo_postulacion', 'estado')
        }),
        ('Información Adicional', {
            'fields': ('mensaje_personalizado', 'tarifa_propuesta')
        }),
        ('Notas del Empleador', {
            'fields': ('notas_empleador',)
        }),
        ('Fechas', {
            'fields': ('fecha_postulacion', 'fecha_respuesta'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'musico', 'oferta_laboral__empleador', 'portafolio'
        )


# Registrar modelos de ofertas
admin.site.register(OfertaInstrumento)
admin.site.register(OfertaGenero)
