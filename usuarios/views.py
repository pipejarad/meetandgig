from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, LoginForm
from .models import Usuario


def inicio(request):
    usuarios = Usuario.objects.all()

    # return HttpResponse("<h1>Meet & Gig</h1>")
    return render(request, 'usuarios/inicio.html', context={'usuarios': usuarios})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirige según tipo de usuario
            if user.tipo_usuario == 'musico':
                return redirect('perfil_musico_crear')
            else:
                return redirect('perfil_empleador_crear')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirige según tipo de usuario
            if user.tipo_usuario == 'musico':
                return redirect('perfil_musico_detalle', pk=user.pk)
            else:
                return redirect('perfil_empleador_detalle', pk=user.pk)
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
