from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import Usuario, PerfilMusico


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
        })
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
    foto_perfil = forms.ImageField(
        required=False,
        label="Foto de perfil",
        help_text="Foto de perfil profesional (recomendado: 400x400px)"
    )
    
    generos_musicales = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Rock, Blues, Jazz',
            'data-toggle': 'tooltip',
            'title': 'Separa los géneros con comas'
        }),
        help_text='Separa los géneros musicales con comas'
    )
    
    instrumentos_secundarios = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Piano, Bajo, Armónica',
            'data-toggle': 'tooltip',
            'title': 'Separa los instrumentos con comas'
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
        model = PerfilMusico
        fields = [
            'biografia', 'instrumento_principal', 'instrumentos_secundarios',
            'generos_musicales', 'nivel_experiencia', 'años_experiencia',
            'formacion_musical', 'website_personal', 'soundcloud_url',
            'youtube_url', 'spotify_url', 'instagram_url', 'facebook_url',
            'ubicacion', 'disponible_para_gigs', 'tarifa_base',
            'video_demo', 'perfil_publico'
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
            'perfil_publico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # No inicializar con la imagen actual - solo mostrar en template
        # para evitar problemas con el widget de archivos
        
        self.fields['foto_perfil'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })
    
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
    
    def save(self, commit=True):
        foto_perfil = self.cleaned_data.get('foto_perfil')
        
        if foto_perfil and self.usuario:
            self.usuario.foto_perfil = foto_perfil
            self.usuario.save()
        
        perfil = super().save(commit=False)
        if commit:
            perfil.save()
        return perfil
