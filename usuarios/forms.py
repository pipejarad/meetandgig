from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tipo_usuario = forms.ChoiceField(
        choices=Usuario._meta.get_field('tipo_usuario').choices)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario',
                  'foto_perfil', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email


class LoginForm(AuthenticationForm):
    pass
