from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('musico', 'Músico'),
        ('empleador', 'Empleador'),
    ]
    
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este email.',
        }
    )
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES,
        verbose_name='Tipo de usuario'
    )
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', 
        null=True, 
        blank=True,
        verbose_name='Foto de perfil'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'tipo_usuario']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# CATÁLOGOS NORMALIZADOS (Ticket 2.11)
class Instrumento(models.Model):
    """Catálogo de instrumentos musicales (tabla existente)"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    categoria = models.CharField(max_length=50, blank=True, verbose_name='Categoría')

    class Meta:
        managed = False  # Django no gestiona esta tabla
        db_table = 'usuarios_instrumento'
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'

    def __str__(self):
        return self.nombre


class Genero(models.Model):
    """Catálogo de géneros musicales (tabla existente)"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    class Meta:
        managed = False  # Django no gestiona esta tabla
        db_table = 'usuarios_generomusical'
        verbose_name = 'Género Musical'
        verbose_name_plural = 'Géneros Musicales'

    def __str__(self):
        return self.nombre


class NivelExperiencia(models.Model):
    """Catálogo de niveles de experiencia musical"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    descripcion = models.CharField(max_length=100, blank=True, verbose_name='Descripción')
    orden = models.PositiveIntegerField(unique=True, verbose_name='Orden')
    años_minimos = models.PositiveIntegerField(default=0, verbose_name='Años mínimos')
    años_maximos = models.PositiveIntegerField(null=True, blank=True, verbose_name='Años máximos')

    class Meta:
        verbose_name = 'Nivel de Experiencia'
        verbose_name_plural = 'Niveles de Experiencia'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    """Catálogo de ubicaciones geográficas"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    region = models.CharField(max_length=50, blank=True, verbose_name='Región')
    pais = models.CharField(max_length=50, default='Chile', verbose_name='País')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['orden', 'region', 'nombre']

    def __str__(self):
        if self.region:
            return f"{self.nombre}, {self.region}"
        return self.nombre


class PerfilMusico(models.Model):
    """Perfil personal y administrativo del músico (NO información profesional)"""
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_musico')
    
    # DATOS PERSONALES/ADMINISTRATIVOS ÚNICAMENTE
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    direccion = models.CharField(max_length=200, blank=True, verbose_name='Dirección')
    
    # CONFIGURACIONES PRIVADAS
    recibir_notificaciones_email = models.BooleanField(
        default=True, 
        verbose_name='Recibir notificaciones por email'
    )
    mostrar_telefono_publico = models.BooleanField(
        default=False, 
        verbose_name='Mostrar teléfono públicamente'
    )
    
    # METADATOS
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Músico'
        verbose_name_plural = 'Perfiles de Músicos'

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"


class PerfilEmpleador(models.Model):
    TIPO_ENTIDAD_CHOICES = [
        ('empresa', 'Empresa'),
        ('fundacion', 'Fundación'),
        ('organizacion_sin_fines_lucro', 'Organización sin fines de lucro'),
        ('institucion_educativa', 'Institución educativa'),
        ('gobierno', 'Gobierno/Institución pública'),
        ('iglesia', 'Iglesia/Organización religiosa'),
        ('club_social', 'Club social'),
        ('restaurante_bar', 'Restaurante/Bar'),
        ('hotel', 'Hotel/Centro de eventos'),
        ('particular', 'Particular'),
        ('otro', 'Otro')
    ]

    TAMAÑO_ORGANIZACION_CHOICES = [
        ('1-10', '1-10 empleados'),
        ('11-50', '11-50 empleados'),
        ('51-200', '51-200 empleados'),
        ('201-500', '201-500 empleados'),
        ('501-1000', '501-1000 empleados'),
        ('1000+', 'Más de 1000 empleados'),
        ('no_aplica', 'No aplica')
    ]

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil_empleador'
    )
    
    nombre_organizacion = models.CharField(
        max_length=200,
        verbose_name='Nombre de la organización'
    )
    tipo_entidad = models.CharField(
        max_length=50,
        choices=TIPO_ENTIDAD_CHOICES,
        verbose_name='Tipo de entidad',
        default='empresa'
    )
    descripcion = models.TextField(
        max_length=1000,
        blank=True,
        help_text='Describe tu organización (máx. 1000 caracteres)',
        verbose_name='Descripción de la organización'
    )
    
    email_corporativo = models.EmailField(
        blank=True,
        verbose_name='Email corporativo',
        help_text='Email oficial de la organización (opcional)'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    contacto_alternativo = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Contacto alternativo',
        help_text='Nombre de persona de contacto'
    )
    
    ubicacion = models.CharField(
        max_length=200,
        verbose_name='Ubicación',
        help_text='Ciudad, región o dirección'
    )
    direccion_completa = models.TextField(
        max_length=300,
        blank=True,
        verbose_name='Dirección completa'
    )
    
    sitio_web = models.URLField(
        blank=True,
        verbose_name='Sitio web'
    )
    linkedin_url = models.URLField(
        blank=True,
        verbose_name='LinkedIn'
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name='Facebook'
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name='Instagram'
    )
    
    año_fundacion = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año de fundación'
    )
    tamaño_organizacion = models.CharField(
        max_length=50,
        choices=TAMAÑO_ORGANIZACION_CHOICES,
        blank=True,
        verbose_name='Tamaño de la organización'
    )
    
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    perfil_verificado = models.BooleanField(
        default=False,
        verbose_name='Perfil verificado'
    )

    class Meta:
        verbose_name = 'Perfil de Empleador'
        verbose_name_plural = 'Perfiles de Empleadores'

    def __str__(self):
        return f"{self.nombre_organizacion} - {self.usuario.get_full_name() or self.usuario.username}"
    
    def get_nombre_completo_contacto(self):
        return self.usuario.get_full_name() or self.usuario.username
    
    def get_email_principal(self):
        return self.email_corporativo or self.usuario.email


class Portafolio(models.Model):
    """Portafolio profesional público del músico"""
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='portafolio')
    slug = models.SlugField(unique=True, max_length=100, verbose_name='Slug público')
    
    # INFORMACIÓN PROFESIONAL
    biografia = models.TextField(
        max_length=1000, 
        blank=True, 
        verbose_name='Biografía profesional',
        help_text='Cuéntanos sobre tu trayectoria musical (máx. 1000 caracteres)'
    )
    formacion_musical = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name='Formación musical',
        help_text='Estudios musicales, cursos, talleres, etc.'
    )
    años_experiencia = models.PositiveIntegerField(
        default=1, 
        verbose_name='Años de experiencia',
        help_text='Número de años tocando música'
    )
    
    # RELACIONES CON CATÁLOGOS NORMALIZADOS
    nivel_experiencia = models.ForeignKey(
        NivelExperiencia, 
        on_delete=models.PROTECT, 
        verbose_name='Nivel de experiencia'
    )
    ubicacion = models.ForeignKey(
        Ubicacion, 
        on_delete=models.PROTECT, 
        verbose_name='Ubicación'
    )
    
    # ENLACES PROFESIONALES
    website_personal = models.URLField(blank=True, verbose_name='Sitio web personal')
    soundcloud_url = models.URLField(blank=True, verbose_name='SoundCloud')
    youtube_url = models.URLField(blank=True, verbose_name='YouTube')
    spotify_url = models.URLField(blank=True, verbose_name='Spotify')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook')
    video_demo = models.URLField(
        blank=True, 
        verbose_name='Video demostración',
        help_text='Enlace a video demo (YouTube, Vimeo, etc.)'
    )
    
    # INFORMACIÓN COMERCIAL
    disponible_para_gigs = models.BooleanField(
        default=True, 
        verbose_name='Disponible para presentaciones'
    )
    tarifa_base = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name='Tarifa base (CLP)',
        help_text='Tarifa base por presentación en pesos chilenos (CLP)'
    )
    
    # FLAGS DE VISIBILIDAD
    show_email = models.BooleanField(default=False, verbose_name='Mostrar email')
    show_social_links = models.BooleanField(default=True, verbose_name='Mostrar enlaces sociales')
    show_education = models.BooleanField(default=True, verbose_name='Mostrar formación')
    show_tarifa = models.BooleanField(default=True, verbose_name='Mostrar tarifa')
    show_telefono = models.BooleanField(default=False, verbose_name='Mostrar teléfono')
    
    # METADATOS
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True, verbose_name='Portafolio activo')

    class Meta:
        verbose_name = 'Portafolio'
        verbose_name_plural = 'Portafolios'

    def __str__(self):
        return f"Portafolio - {self.usuario.get_full_name() or self.usuario.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.usuario.get_full_name() or self.usuario.username)
            slug = base_slug
            counter = 1
            while Portafolio.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_instrumentos_principales(self):
        """Retorna los instrumentos marcados como principales"""
        return self.portafolio_instrumentos.filter(es_principal=True).select_related('instrumento')

    def get_instrumentos_secundarios(self):
        """Retorna los instrumentos secundarios"""
        return self.portafolio_instrumentos.filter(es_principal=False).select_related('instrumento')

    def get_generos(self):
        """Retorna todos los géneros del portafolio"""
        return self.portafolio_generos.all().select_related('genero')

    @property
    def instrumentos(self):
        """Property para acceso fácil a instrumentos - para compatibilidad"""
        from django.db.models import Q
        return Instrumento.objects.filter(
            Q(portafolioinstrumento__portafolio=self)
        ).distinct()

    @property 
    def generos(self):
        """Property para acceso fácil a géneros - para compatibilidad"""
        from django.db.models import Q
        return Genero.objects.filter(
            Q(portafoliogenero__portafolio=self)  
        ).distinct()

    def get_enlaces_sociales(self):
        """Retorna lista de enlaces sociales no vacíos con iconos"""
        if not self.show_social_links:
            return []
        
        enlaces = []
        
        if self.website_personal:
            enlaces.append({
                'nombre': 'Sitio Web Personal',
                'url': self.website_personal,
                'icon': 'fas fa-globe'
            })
            
        if self.youtube_url:
            enlaces.append({
                'nombre': 'YouTube',
                'url': self.youtube_url,
                'icon': 'fab fa-youtube'
            })
            
        if self.soundcloud_url:
            enlaces.append({
                'nombre': 'SoundCloud',
                'url': self.soundcloud_url,
                'icon': 'fab fa-soundcloud'
            })
            
        if self.spotify_url:
            enlaces.append({
                'nombre': 'Spotify',
                'url': self.spotify_url,
                'icon': 'fab fa-spotify'
            })
            
        if self.instagram_url:
            enlaces.append({
                'nombre': 'Instagram',
                'url': self.instagram_url,
                'icon': 'fab fa-instagram'
            })
            
        if self.facebook_url:
            enlaces.append({
                'nombre': 'Facebook',
                'url': self.facebook_url,
                'icon': 'fab fa-facebook'
            })
            
        return enlaces


# TABLAS INTERMEDIAS (M2M con metadata)
class PortafolioInstrumento(models.Model):
    """Relación entre portafolio e instrumentos con metadata"""
    portafolio = models.ForeignKey(
        Portafolio, 
        on_delete=models.CASCADE, 
        related_name='portafolio_instrumentos'
    )
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    es_principal = models.BooleanField(default=False, verbose_name='Es instrumento principal')
    prioridad = models.PositiveIntegerField(default=1, verbose_name='Prioridad')
    años_experiencia = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name='Años de experiencia con este instrumento'
    )

    class Meta:
        verbose_name = 'Instrumento del Portafolio'
        verbose_name_plural = 'Instrumentos del Portafolio'
        unique_together = [('portafolio', 'instrumento')]
        ordering = ['prioridad', '-es_principal']

    def __str__(self):
        tipo = "Principal" if self.es_principal else "Secundario"
        return f"{self.portafolio.usuario.username} - {self.instrumento.nombre} ({tipo})"


class PortafolioGenero(models.Model):
    """Relación entre portafolio y géneros musicales"""
    portafolio = models.ForeignKey(
        Portafolio, 
        on_delete=models.CASCADE, 
        related_name='portafolio_generos'
    )
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    prioridad = models.PositiveIntegerField(default=1, verbose_name='Prioridad')

    class Meta:
        verbose_name = 'Género del Portafolio'
        verbose_name_plural = 'Géneros del Portafolio'
        unique_together = [('portafolio', 'genero')]
        ordering = ['prioridad']

    def __str__(self):
        return f"{self.portafolio.usuario.username} - {self.genero.nombre}"


class Multimedia(models.Model):
    """Multimedia del portafolio (imágenes y enlaces a videos/audio)"""
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video_youtube', 'Video de YouTube'),
        ('video_vimeo', 'Video de Vimeo'),
        ('audio_soundcloud', 'Audio de SoundCloud'),
        ('audio_spotify', 'Audio de Spotify'),
    ]

    portafolio = models.ForeignKey(
        Portafolio, 
        on_delete=models.CASCADE, 
        related_name='multimedia'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    titulo = models.CharField(max_length=100, verbose_name='Título')
    descripcion = models.TextField(max_length=300, blank=True, verbose_name='Descripción')
    
    # Para imágenes
    imagen = models.ImageField(
        upload_to='portafolios/multimedia/', 
        null=True, 
        blank=True, 
        verbose_name='Imagen'
    )
    
    # Para enlaces externos
    url = models.URLField(blank=True, verbose_name='URL')
    
    orden = models.PositiveIntegerField(default=1, verbose_name='Orden')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Multimedia'
        verbose_name_plural = 'Multimedia'
        ordering = ['orden', '-fecha_creacion']

    def __str__(self):
        return f"{self.portafolio.usuario.username} - {self.titulo}"


class Testimonio(models.Model):
    """Testimonios y referencias en el portafolio"""
    portafolio = models.ForeignKey(
        Portafolio, 
        on_delete=models.CASCADE, 
        related_name='testimonios'
    )
    autor_nombre = models.CharField(max_length=100, verbose_name='Nombre del autor')
    autor_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Usuario autor (opcional)',
        help_text='Si el testimonio es de un usuario registrado'
    )
    texto = models.TextField(max_length=500, verbose_name='Testimonio')
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de publicación')
    verificado = models.BooleanField(default=False, verbose_name='Verificado')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return f"Testimonio de {self.autor_nombre} para {self.portafolio.usuario.username}"
