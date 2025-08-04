from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from .forms import RegistroForm, LoginForm, RecuperarPasswordForm, CambiarPasswordForm, PerfilMusicoForm, PerfilEmpleadorForm
from .models import Usuario, PerfilMusico, PerfilEmpleador


def inicio(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/inicio.html', context={'usuarios': usuarios})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(
                    request, 
                    f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.'
                )
                # Especificar el backend para el login
                login(request, user, backend='usuarios.backends.EmailBackend')
                return _redirect_by_user_type(user)
            except Exception as e:
                messages.error(request, 'Ocurrió un error al crear la cuenta. Intenta nuevamente.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            return _redirect_by_user_type(user)
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f'Hasta luego, {username}. Has cerrado sesión correctamente.')
    return redirect('login')


def _redirect_by_user_type(user):
    """
    Función helper para redirigir usuarios según su tipo.
    Sigue el principio DRY para evitar duplicación de lógica.
    """
    if user.tipo_usuario == 'musico':
        # TODO: Implementar estas vistas en próximos tickets  
        return redirect('inicio')  # Temporal hasta crear perfil_musico_crear
    else:
        # TODO: Implementar estas vistas en próximos tickets
        return redirect('inicio')  # Temporal hasta crear perfil_empleador_crear


def recuperar_password_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = RecuperarPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Usuario.objects.get(email__iexact=email)
                _send_password_reset_email(request, user)
                messages.success(
                    request, 
                    'Se ha enviado un enlace de recuperación a tu email. Revisa tu bandeja de entrada.'
                )
                return redirect('login')
            except Usuario.DoesNotExist:
                messages.error(request, 'No existe un usuario con este email.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RecuperarPasswordForm()
    
    return render(request, 'usuarios/recuperar_password.html', {'form': form})


def cambiar_password_view(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect('inicio')
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'El enlace de recuperación es inválido o ha expirado.')
        return redirect('recuperar_password')

    if request.method == 'POST':
        form = CambiarPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Tu contraseña ha sido cambiada exitosamente. Ya puedes iniciar sesión.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CambiarPasswordForm(user)

    return render(request, 'usuarios/cambiar_password.html', {'form': form})


def _send_password_reset_email(request, user):
    """
    Función helper para enviar email de recuperación de contraseña.
    Mantiene la lógica de envío centralizada siguiendo DRY.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_url = request.build_absolute_uri(
        reverse('cambiar_password', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = 'Recuperación de contraseña - Meet & Gig'
    message = f"""
Hola {user.username},

Has solicitado recuperar tu contraseña en Meet & Gig.

Haz clic en el siguiente enlace para cambiar tu contraseña:
{reset_url}

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
El equipo de Meet & Gig
"""
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@login_required
def editar_perfil_musico(request):
    if request.user.tipo_usuario != 'musico':
        messages.error(request, 'Solo los músicos pueden acceder a esta sección.')
        return redirect('inicio')
    
    try:
        perfil = request.user.perfil_musico
    except PerfilMusico.DoesNotExist:
        perfil = None
    
    if request.method == 'POST':
        form = PerfilMusicoForm(request.POST, request.FILES, instance=perfil, usuario=request.user)
        if form.is_valid():
            perfil = form.save(commit=False)
            if not perfil.usuario_id:
                perfil.usuario = request.user
            perfil.save()
            
            request.user.refresh_from_db()
            
            if form.cleaned_data.get('foto_perfil'):
                messages.success(request, '✅ Perfil e imagen actualizados exitosamente.')
            else:
                messages.success(request, '✅ Perfil actualizado exitosamente.')
            
            return redirect('editar_perfil_musico')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PerfilMusicoForm(instance=perfil, usuario=request.user)
    
    context = {
        'form': form,
        'perfil': perfil,
        'usuario': request.user,
        'es_nuevo_perfil': perfil is None
    }
    
    return render(request, 'usuarios/editar_perfil_musico.html', context)


@login_required 
def ver_mi_perfil(request):
    if request.user.tipo_usuario != 'musico':
        messages.error(request, 'Solo los músicos tienen perfil público.')
        return redirect('inicio')
    
    try:
        perfil = request.user.perfil_musico
    except PerfilMusico.DoesNotExist:
        messages.info(
            request, 
            'Aún no has creado tu perfil de músico. ¡Complétalo para que otros puedan encontrarte!'
        )
        return redirect('editar_perfil_musico')
    
    context = {
        'perfil': perfil,
        'usuario': request.user,
        'es_mi_perfil': True
    }
    
    return render(request, 'usuarios/ver_perfil_musico.html', context)


class EmpleadorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.tipo_usuario != 'empleador':
            raise PermissionDenied("Solo los empleadores pueden acceder a esta página.")
        
        return super().dispatch(request, *args, **kwargs)


class CrearPerfilEmpleadorView(LoginRequiredMixin, EmpleadorRequiredMixin, CreateView):
    model = PerfilEmpleador
    form_class = PerfilEmpleadorForm
    template_name = 'usuarios/crear_perfil_empleador.html'
    success_url = reverse_lazy('perfil_empleador')

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'perfil_empleador'):
            return redirect('editar_perfil_empleador')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Perfil de empleador creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Perfil de Empleador'
        context['boton_texto'] = 'Crear Perfil'
        return context


class EditarPerfilEmpleadorView(LoginRequiredMixin, EmpleadorRequiredMixin, UpdateView):
    model = PerfilEmpleador
    form_class = PerfilEmpleadorForm
    template_name = 'usuarios/editar_perfil_empleador.html'
    success_url = reverse_lazy('perfil_empleador')

    def get_object(self):
        return get_object_or_404(PerfilEmpleador, usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Perfil de Empleador'
        context['boton_texto'] = 'Actualizar Perfil'
        return context


@login_required
def perfil_empleador_view(request):
    if request.user.tipo_usuario != 'empleador':
        raise PermissionDenied("Solo los empleadores pueden ver esta página.")
    
    try:
        perfil = request.user.perfil_empleador
    except PerfilEmpleador.DoesNotExist:
        return redirect('crear_perfil_empleador')
    
    context = {
        'perfil': perfil,
        'usuario': request.user
    }
    return render(request, 'usuarios/perfil_empleador.html', context)
