from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=Usuario._meta.get_field('tipo_usuario').choices)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario',
                  'foto_perfil', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass
