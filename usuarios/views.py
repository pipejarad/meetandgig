from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from .forms import RegistroForm, LoginForm
from .models import Usuario


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
