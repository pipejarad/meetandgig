from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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


class PerfilMusico(models.Model):
    GENEROS_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('jazz', 'Jazz'),
        ('blues', 'Blues'),
        ('country', 'Country'),
        ('folk', 'Folk'),
        ('reggae', 'Reggae'),
        ('latin', 'Música Latina'),
        ('classical', 'Clásica'),
        ('electronic', 'Electrónica'),
        ('indie', 'Indie'),
        ('alternative', 'Alternativo'),
        ('punk', 'Punk'),
        ('metal', 'Metal'),
        ('hip_hop', 'Hip Hop'),
        ('r_and_b', 'R&B'),
        ('otro', 'Otro')
    ]
    
    INSTRUMENTOS_CHOICES = [
        ('guitarra', 'Guitarra'),
        ('bajo', 'Bajo'),
        ('bateria', 'Batería'),
        ('piano', 'Piano'),
        ('teclados', 'Teclados'),
        ('violin', 'Violín'),
        ('saxofon', 'Saxofón'),
        ('trompeta', 'Trompeta'),
        ('flauta', 'Flauta'),
        ('voz', 'Voz/Canto'),
        ('armonica', 'Armónica'),
        ('ukulele', 'Ukulele'),
        ('mandolina', 'Mandolina'),
        ('acordeon', 'Acordeón'),
        ('otro', 'Otro')
    ]
    
    NIVEL_EXPERIENCIA_CHOICES = [
        ('principiante', 'Principiante (0-2 años)'),
        ('intermedio', 'Intermedio (3-5 años)'),
        ('avanzado', 'Avanzado (6-10 años)'),
        ('profesional', 'Profesional (10+ años)')
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_musico')
    
    # Información básica profesional
    biografia = models.TextField(
        max_length=1000, 
        help_text='Cuéntanos sobre tu trayectoria musical (máx. 1000 caracteres)',
        blank=True
    )
    
    # Instrumentos y géneros (selección múltiple)
    instrumento_principal = models.CharField(
        max_length=50, 
        choices=INSTRUMENTOS_CHOICES,
        verbose_name='Instrumento principal',
        default='guitarra'
    )
    instrumentos_secundarios = models.CharField(
        max_length=200,
        blank=True,
        help_text='Otros instrumentos que tocas (separados por comas)',
        verbose_name='Instrumentos secundarios'
    )
    generos_musicales = models.CharField(
        max_length=200,
        help_text='Géneros musicales que interpretas (separados por comas)',
        verbose_name='Géneros musicales',
        default='rock'
    )
    
    # Experiencia y formación
    nivel_experiencia = models.CharField(
        max_length=20,
        choices=NIVEL_EXPERIENCIA_CHOICES,
        verbose_name='Nivel de experiencia',
        default='principiante'
    )
    años_experiencia = models.PositiveIntegerField(
        verbose_name='Años de experiencia',
        help_text='Número de años tocando música',
        default=1
    )
    formacion_musical = models.TextField(
        max_length=500,
        blank=True,
        help_text='Estudios musicales, cursos, talleres, etc.',
        verbose_name='Formación musical'
    )
    
    # Enlaces externos
    website_personal = models.URLField(blank=True, verbose_name='Sitio web personal')
    soundcloud_url = models.URLField(blank=True, verbose_name='SoundCloud')
    youtube_url = models.URLField(blank=True, verbose_name='YouTube')
    spotify_url = models.URLField(blank=True, verbose_name='Spotify')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook')
    
    # Información profesional
    ubicacion = models.CharField(
        max_length=100, 
        verbose_name='Ubicación',
        default='No especificada'
    )
    disponible_para_gigs = models.BooleanField(
        default=True, 
        verbose_name='Disponible para presentaciones'
    )
    tarifa_base = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text='Tarifa base por presentación en pesos chilenos (CLP)',
        verbose_name='Tarifa base (CLP)'
    )
    
    # Material multimedia
    video_demo = models.URLField(
        blank=True,
        help_text='Enlace a video demo (YouTube, Vimeo, etc.)',
        verbose_name='Video demostración'
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    perfil_publico = models.BooleanField(
        default=True,
        help_text='¿Deseas que tu perfil sea visible públicamente?',
        verbose_name='Perfil público'
    )

    class Meta:
        verbose_name = 'Perfil de Músico'
        verbose_name_plural = 'Perfiles de Músicos'

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
    
    def get_instrumentos_list(self):
        """Retorna lista de instrumentos como array"""
        instrumentos = [self.get_instrumento_principal_display()]
        if self.instrumentos_secundarios:
            instrumentos.extend([i.strip() for i in self.instrumentos_secundarios.split(',')])
        return instrumentos
    
    def get_generos_list(self):
        """Retorna lista de géneros como array"""
        if self.generos_musicales:
            return [g.strip() for g in self.generos_musicales.split(',')]
        return []


class PerfilEmpleador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_organizacion = models.CharField(max_length=100)
    tipo_entidad = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    contacto_alternativo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.usuario.username
