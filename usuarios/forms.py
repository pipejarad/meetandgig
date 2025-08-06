from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image
from .models import Usuario, PerfilMusico, PerfilEmpleador, PortafolioMusico


def validate_image_file(image):
    """Valida que el archivo de imagen sea válido y tenga un tamaño apropiado"""
    if image:
        # Validar tamaño de archivo (máximo 5MB)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError("La imagen no puede ser mayor a 5MB.")
        
        # Validar que sea una imagen válida
        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            raise ValidationError("El archivo debe ser una imagen válida (JPG, PNG, GIF).")
        
        # Validar dimensiones mínimas
        image.seek(0)  # Reset el puntero del archivo
        img = Image.open(image)
        width, height = img.size
        if width < 100 or height < 100:
            raise ValidationError("La imagen debe tener al menos 100x100 píxeles.")
        
        # Validar formato
        if img.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
            raise ValidationError("Solo se permiten archivos JPG, PNG o GIF.")
    
    return image


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        error_messages={
            'required': 'El email es obligatorio.',
            'invalid': 'Ingresa un email válido.',
        }
    )
    
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        error_messages={
            'required': 'Debes seleccionar un tipo de usuario.',
        }
    )
    
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        validators=[validate_image_file],
        help_text='Imagen de perfil (máx. 5MB, mín. 100x100px, formatos: JPG, PNG, GIF)'
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
    )
    
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario único'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario', 'foto_perfil', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
            
        if Usuario.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email.lower()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username
            
        if Usuario.objects.filter(username__iexact=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email o nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com o nombre de usuario'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña'
        })
    )


class RecuperarPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        error_messages={
            'required': 'El email es obligatorio.',
            'invalid': 'Ingresa un email válido.',
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
            
        if not Usuario.objects.filter(email__iexact=email).exists():
            raise ValidationError("No existe un usuario registrado con este email.")
        return email.lower()


class CambiarPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='Tu contraseña debe tener al menos 8 caracteres.'
    )
    
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )


class PerfilMusicoForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    foto_perfil = forms.ImageField(
        required=False,
        label="Foto de perfil",
        help_text="Imagen de perfil (máx. 5MB, mín. 100x100px, formatos: JPG, PNG, GIF)",
        validators=[validate_image_file]
    )
    
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        }),
        help_text='Número de teléfono personal'
    )
    
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle, número, comuna, ciudad',
            'maxlength': 200
        }),
        help_text='Dirección personal (opcional)'
    )
    
    contacto_emergencia = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre: Teléfono',
            'maxlength': 100
        }),
        help_text='Contacto de emergencia (opcional)'
    )

    class Meta:
        model = PerfilMusico
        fields = [
            'telefono', 'fecha_nacimiento', 'direccion', 'contacto_emergencia',
            'recibir_notificaciones_email', 'mostrar_telefono_publico'
        ]
        
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'recibir_notificaciones_email': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'mostrar_telefono_publico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            self.fields['first_name'].initial = self.usuario.first_name
            self.fields['last_name'].initial = self.usuario.last_name
            if hasattr(self.usuario, 'foto_perfil'):
                self.fields['foto_perfil'].initial = self.usuario.foto_perfil
        
        self.fields['foto_perfil'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if telefono and len(telefono.replace(' ', '').replace('+', '').replace('-', '')) < 8:
            raise forms.ValidationError('El teléfono debe tener al menos 8 dígitos.')
        return telefono
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        if not perfil.usuario_id:
            perfil.usuario = self.usuario
        
        if commit:
            perfil.save()
            
            if self.usuario:
                self.usuario.first_name = self.cleaned_data.get('first_name', '')
                self.usuario.last_name = self.cleaned_data.get('last_name', '')
                
                if self.cleaned_data.get('foto_perfil'):
                    self.usuario.foto_perfil = self.cleaned_data['foto_perfil']
                
                self.usuario.save()
        
        return perfil


class PortafolioMusicoForm(forms.ModelForm):
    generos_musicales = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Rock, Blues, Jazz'
        }),
        help_text='Separa los géneros musicales con comas'
    )
    
    instrumentos_secundarios = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Piano, Bajo, Armónica'
        }),
        help_text='Otros instrumentos que tocas (separados por comas)'
    )
    
    biografia = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Cuéntanos sobre tu trayectoria musical, experiencias destacadas, influencias...',
            'maxlength': 1000
        })
    )
    
    formacion_musical = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Estudios formales, cursos, talleres, profesores destacados...',
            'maxlength': 500
        })
    )
    
    tarifa_base = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '150000',
            'step': '1000',
            'min': '0'
        }),
        help_text='Tarifa base por presentación en pesos chilenos (CLP, sin decimales)'
    )

    class Meta:
        model = PortafolioMusico
        fields = [
            'biografia', 'instrumento_principal', 'instrumentos_secundarios',
            'generos_musicales', 'nivel_experiencia', 'años_experiencia',
            'formacion_musical', 'website_personal', 'soundcloud_url',
            'youtube_url', 'spotify_url', 'instagram_url', 'facebook_url',
            'ubicacion', 'disponible_para_gigs', 'tarifa_base',
            'video_demo', 'portafolio_publico'
        ]
        
        widgets = {
            'instrumento_principal': forms.Select(attrs={'class': 'form-select'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-select'}),
            'años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '80'
            }),
            'website_personal': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://tu-sitio-web.com'
            }),
            'soundcloud_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://soundcloud.com/tu-perfil'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/tu-canal'
            }),
            'spotify_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://open.spotify.com/artist/...'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/tu-usuario'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/tu-pagina'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad, País'
            }),
            'disponible_para_gigs': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'video_demo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'portafolio_publico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_generos_musicales(self):
        generos = self.cleaned_data.get('generos_musicales', '')
        if generos:
            generos_list = [g.strip() for g in generos.split(',') if g.strip()]
            if len(generos_list) > 10:
                raise ValidationError("Máximo 10 géneros musicales permitidos.")
            return ', '.join(generos_list)
        return generos
    
    def clean_instrumentos_secundarios(self):
        instrumentos = self.cleaned_data.get('instrumentos_secundarios', '')
        if instrumentos:
            instrumentos_list = [i.strip() for i in instrumentos.split(',') if i.strip()]
            if len(instrumentos_list) > 8:
                raise ValidationError("Máximo 8 instrumentos secundarios permitidos.")
            return ', '.join(instrumentos_list)
        return instrumentos
    
    def clean_años_experiencia(self):
        años = self.cleaned_data.get('años_experiencia')
        if años is not None and años > 80:
            raise ValidationError("Los años de experiencia no pueden exceder 80.")
        return años


class PerfilEmpleadorForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    foto_perfil = forms.ImageField(
        required=False,
        label='Foto de perfil',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[validate_image_file],
        help_text='Imagen de perfil (máx. 5MB, mín. 100x100px, formatos: JPG, PNG, GIF)'
    )

    class Meta:
        model = PerfilEmpleador
        fields = [
            'nombre_organizacion', 'tipo_entidad', 'descripcion',
            'email_corporativo', 'telefono', 'contacto_alternativo',
            'ubicacion', 'direccion_completa', 'sitio_web',
            'linkedin_url', 'facebook_url', 'instagram_url',
            'año_fundacion', 'tamaño_organizacion'
        ]
        widgets = {
            'nombre_organizacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_entidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email_corporativo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_alternativo': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_completa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'año_fundacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'tamaño_organizacion': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['foto_perfil'].initial = user.foto_perfil

    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        if commit:
            user = perfil.usuario
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            
            if self.cleaned_data['foto_perfil']:
                user.foto_perfil = self.cleaned_data['foto_perfil']
            
            user.save()
            perfil.save()
        
        return perfil

    def clean_año_fundacion(self):
        año = self.cleaned_data.get('año_fundacion')
        if año and (año < 1800 or año > timezone.now().year):
            raise forms.ValidationError('El año de fundación debe estar entre 1800 y el año actual.')
        return año
