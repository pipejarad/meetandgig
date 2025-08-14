from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
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
from django.views.generic import CreateView, UpdateView, DetailView
from django.core.exceptions import PermissionDenied
from .forms import (
    RegistroForm, LoginForm, RecuperarPasswordForm, CambiarPasswordForm, 
    PerfilMusicoForm, PerfilEmpleadorForm, PortafolioForm, CrearOfertaLaboralForm
)
from .models import Usuario, PerfilMusico, PerfilEmpleador, Portafolio, OfertaLaboral


def inicio(request):
    portafolios_destacados = Portafolio.objects.filter(
        activo=True,
        disponible_para_gigs=True
    ).select_related('usuario', 'ubicacion').prefetch_related(
        'portafolio_instrumentos__instrumento',
        'portafolio_generos__genero'
    ).order_by('-fecha_actualizacion')[:6]
    
    stats = {
        'total_musicos': Usuario.objects.filter(tipo_usuario='musico').count(),
        'total_empleadores': Usuario.objects.filter(tipo_usuario='empleador').count(),
        'total_portafolios': Portafolio.objects.filter(activo=True).count(),
        'total_usuarios': Usuario.objects.count(),
    }
    
    context = {
        'portafolios_destacados': portafolios_destacados,
        'stats': stats,
    }
    
    return render(request, 'usuarios/inicio.html', context)


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
            perfil = form.save()
            
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


# ================================================
# VISTAS DEL PORTAFOLIO MÚSICO
# ================================================

@login_required
def ver_mi_portafolio(request):
    """Vista que redirige al músico a su portafolio unificado"""
    if request.user.tipo_usuario != 'musico':
        raise PermissionDenied("Solo los músicos pueden ver esta página.")
    
    try:
        portafolio = Portafolio.objects.get(usuario=request.user)
    except Portafolio.DoesNotExist:
        # Crear portafolio básico si no existe
        from usuarios.models import NivelExperiencia, Ubicacion
        
        nivel_default = NivelExperiencia.objects.filter(nombre='Principiante').first() or NivelExperiencia.objects.first()
        ubicacion_default = Ubicacion.objects.filter(nombre='Santiago').first() or Ubicacion.objects.first()
            
        portafolio = Portafolio.objects.create(
            usuario=request.user,
            biografia='',
            años_experiencia=1,
            nivel_experiencia=nivel_default,
            ubicacion=ubicacion_default,
            disponible_para_gigs=True,
        )
        messages.success(request, 'Se ha creado tu portafolio básico. ¡Complétalo para destacar!')
    
    return redirect('ver_portafolio', slug=portafolio.slug)


@login_required
def editar_portafolio_musico(request):
    """Vista para editar el portafolio del músico"""
    if request.user.tipo_usuario != 'musico':
        raise PermissionDenied("Solo los músicos pueden editar portafolios.")
    
    try:
        portafolio = Portafolio.objects.get(usuario=request.user)
        created = False
    except Portafolio.DoesNotExist:
        # Obtener valores por defecto
        from usuarios.models import NivelExperiencia, Ubicacion
        
        nivel_default = NivelExperiencia.objects.filter(nombre='Principiante').first()
        ubicacion_default = Ubicacion.objects.filter(nombre='Santiago').first()
        
        if not nivel_default:
            nivel_default = NivelExperiencia.objects.first()
        if not ubicacion_default:
            ubicacion_default = Ubicacion.objects.first()
            
        portafolio = Portafolio.objects.create(
            usuario=request.user,
            biografia='',
            años_experiencia=1,
            nivel_experiencia=nivel_default,
            ubicacion=ubicacion_default,
            disponible_para_gigs=True,
        )
        created = True
    
    es_creacion = created or not any([
        portafolio.biografia, 
        portafolio.formacion_musical,
        portafolio.website_personal
    ])
    
    if request.method == 'POST':
        form = PortafolioForm(request.POST, instance=portafolio)
        if form.is_valid():
            form.save()
            mensaje = 'Portafolio creado exitosamente.' if es_creacion else 'Portafolio actualizado exitosamente.'
            messages.success(request, mensaje)
            return redirect('ver_mi_portafolio')
    else:
        form = PortafolioForm(instance=portafolio)
    
    titulo = 'Crear Mi Portafolio Musical' if es_creacion else 'Editar Mi Portafolio Musical'
    
    context = {
        'form': form,
        'portafolio': portafolio,
        'titulo': titulo,
        'es_creacion': es_creacion
    }
    return render(request, 'usuarios/editar_portafolio_musico.html', context)


def ver_perfil_musico(request, username):
    """Vista pública del perfil de un músico"""
    usuario = get_object_or_404(Usuario, username=username, tipo_usuario='musico')
    
    try:
        perfil = usuario.perfil_musico
    except PerfilMusico.DoesNotExist:
        raise Http404("Este músico no tiene un perfil disponible.")
    
    context = {
        'perfil': perfil,
        'usuario': usuario,
        'es_mi_perfil': request.user.is_authenticated and request.user == usuario,
        'titulo': f'Perfil de {usuario.get_full_name() or usuario.username}'
    }
    return render(request, 'usuarios/ver_perfil_musico.html', context)


def buscar_portafolios(request):
    """Vista de búsqueda y listado de portafolios musicales"""
    from django.core.paginator import Paginator
    from django.db.models import Q
    from .models import Instrumento, Genero, NivelExperiencia, Ubicacion
    
    portafolios = Portafolio.objects.filter(activo=True).select_related(
        'usuario', 'ubicacion', 'nivel_experiencia'
    ).prefetch_related(
        'portafolio_instrumentos__instrumento',
        'portafolio_generos__genero'
    )
    
    # Obtener parámetros de búsqueda
    query = request.GET.get('q', '')
    instrumento_id = request.GET.get('instrumento', '')
    genero_id = request.GET.get('genero', '')
    ubicacion_id = request.GET.get('ubicacion', '')
    nivel_id = request.GET.get('nivel_experiencia', '')
    disponible = request.GET.get('disponible', '')
    tarifa_min = request.GET.get('tarifa_min', '')
    tarifa_max = request.GET.get('tarifa_max', '')
    ordenar = request.GET.get('orden', 'recientes')
    
    # Filtros de búsqueda por texto
    if query:
        portafolios = portafolios.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(biografia__icontains=query) |
            Q(formacion_musical__icontains=query)
        )
    
    # Filtros por instrumento (M2M)
    if instrumento_id:
        portafolios = portafolios.filter(
            portafolio_instrumentos__instrumento_id=instrumento_id
        ).distinct()
    
    # Filtros por género (M2M)
    if genero_id:
        portafolios = portafolios.filter(
            portafolio_generos__genero_id=genero_id
        ).distinct()
    
    # Filtros por ubicación (FK)
    if ubicacion_id:
        portafolios = portafolios.filter(ubicacion_id=ubicacion_id)
    
    # Filtros por nivel de experiencia (FK)
    if nivel_id:
        portafolios = portafolios.filter(nivel_experiencia_id=nivel_id)
    
    # Filtro por disponibilidad
    if disponible == 'true':
        portafolios = portafolios.filter(disponible_para_gigs=True)
    
    # Filtros por rango de tarifas
    if tarifa_min:
        try:
            portafolios = portafolios.filter(tarifa_base__gte=int(tarifa_min))
        except ValueError:
            pass
    
    if tarifa_max:
        try:
            portafolios = portafolios.filter(tarifa_base__lte=int(tarifa_max))
        except ValueError:
            pass
    
    # Ordenamiento
    if ordenar == 'nombre':
        portafolios = portafolios.order_by('usuario__first_name', 'usuario__last_name')
    elif ordenar == 'experiencia':
        portafolios = portafolios.order_by('-años_experiencia')
    elif ordenar == 'tarifa_asc':
        portafolios = portafolios.filter(tarifa_base__isnull=False).order_by('tarifa_base')
    elif ordenar == 'tarifa_desc':
        portafolios = portafolios.filter(tarifa_base__isnull=False).order_by('-tarifa_base')
    else:  # 'recientes' por defecto
        portafolios = portafolios.order_by('-fecha_actualizacion')
    
    # Paginación
    paginator = Paginator(portafolios, 12)
    page_number = request.GET.get('page')
    portafolios_page = paginator.get_page(page_number)
    
    # Obtener opciones para filtros
    instrumentos = Instrumento.objects.all().order_by('nombre')
    generos = Genero.objects.all().order_by('nombre')
    ubicaciones = Ubicacion.objects.filter(activo=True).order_by('nombre')
    niveles_experiencia = NivelExperiencia.objects.all().order_by('orden')
    
    context = {
        'portafolios': portafolios_page,
        'instrumentos': instrumentos,
        'generos': generos,
        'ubicaciones': ubicaciones,
        'niveles_experiencia': niveles_experiencia,
        'filtros_aplicados': {
            'query': query,
            'instrumento_id': instrumento_id,
            'genero_id': genero_id,
            'ubicacion_id': ubicacion_id,
            'nivel_id': nivel_id,
            'disponible': disponible,
            'tarifa_min': tarifa_min,
            'tarifa_max': tarifa_max,
            'ordenar': ordenar,
        },
        'total_resultados': paginator.count,
        'titulo': 'Buscar Músicos',
    }
    
    return render(request, 'usuarios/buscar_portafolios.html', context)


class PortafolioUnificadoView(DetailView):
    model = Portafolio
    template_name = 'usuarios/portafolio_publico.html'
    slug_field = 'slug'
    context_object_name = 'portafolio'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portafolio = self.get_object()
        
        # Detectar si el usuario es propietario del portafolio
        context['es_propietario'] = (
            self.request.user.is_authenticated and 
            self.request.user == portafolio.usuario
        )
        
        # SEO data
        nombre_completo = portafolio.usuario.get_full_name() or portafolio.usuario.username
        context['seo_title'] = f"{nombre_completo} - Músico en Meet&Gig"
        biografia_truncada = portafolio.biografia[:160] if portafolio.biografia else "Músico profesional en Meet&Gig"
        context['seo_description'] = biografia_truncada
        context['seo_keywords'] = self._generate_keywords(portafolio)
        context['canonical_url'] = self.request.build_absolute_uri()
        
        return context
    
    def _generate_keywords(self, portafolio):
        keywords = []
        try:
            keywords.extend([inst.nombre for inst in portafolio.instrumentos.all()])
            keywords.extend([gen.nombre for gen in portafolio.generos.all()])
        except Exception:
            keywords.extend(['músico', 'música'])
            
        if portafolio.ubicacion:
            keywords.append(f"músico {portafolio.ubicacion}")
        
        keywords.extend(['meet&gig', 'portafolio musical'])
        
        return ", ".join(keywords[:10])


# VISTAS PARA OFERTAS LABORALES (Sprint 3)
@login_required
def crear_oferta_laboral_view(request):
    """Vista para crear ofertas laborales (solo empleadores)"""
    
    # Verificar que sea empleador
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden crear ofertas laborales.')
        return redirect('inicio')
    
    # Verificar que tenga perfil de empleador
    try:
        perfil_empleador = request.user.perfil_empleador
    except PerfilEmpleador.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de empleador antes de crear ofertas.')
        return redirect('crear_perfil_empleador')
    
    if request.method == 'POST':
        form = CrearOfertaLaboralForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=True, empleador=perfil_empleador)
            messages.success(
                request, 
                f'Oferta "{oferta.titulo}" creada exitosamente como borrador. Puedes publicarla cuando esté lista.'
            )
            return redirect('ver_mis_ofertas')
    else:
        form = CrearOfertaLaboralForm()
    
    context = {
        'form': form,
        'perfil_empleador': perfil_empleador,
        'titulo_pagina': 'Crear Nueva Oferta Laboral'
    }
    
    return render(request, 'usuarios/crear_oferta_laboral.html', context)


@login_required 
def ver_mis_ofertas_view(request):
    """Vista para que empleadores vean sus ofertas laborales"""
    
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden acceder a esta sección.')
        return redirect('inicio')
    
    try:
        perfil_empleador = request.user.perfil_empleador
        ofertas = OfertaLaboral.objects.filter(empleador=perfil_empleador).order_by('-fecha_creacion')
    except PerfilEmpleador.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de empleador.')
        return redirect('crear_perfil_empleador')
    
    context = {
        'ofertas': ofertas,
        'perfil_empleador': perfil_empleador,
        'titulo_pagina': 'Mis Ofertas Laborales'
    }
    
    return render(request, 'usuarios/mis_ofertas.html', context)


@login_required 
def detalle_oferta_view(request, slug):
    """Vista de detalle de una oferta laboral"""
    oferta = get_object_or_404(OfertaLaboral, slug=slug)
    
    if request.user.tipo_usuario == 'empleador':
        if oferta.empleador != request.user.perfil_empleador:
            messages.error(request, 'No tienes permisos para ver esta oferta.')
            return redirect('ver_mis_ofertas')
    
    context = {
        'oferta': oferta,
        'titulo_pagina': oferta.titulo
    }
    
    return render(request, 'usuarios/detalle_oferta.html', context)


@login_required
def editar_oferta_view(request, slug):
    """Vista para editar una oferta laboral existente"""
    oferta = get_object_or_404(OfertaLaboral, slug=slug)
    
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden editar ofertas.')
        return redirect('inicio')
    
    if oferta.empleador != request.user.perfil_empleador:
        messages.error(request, 'No tienes permisos para editar esta oferta.')
        return redirect('ver_mis_ofertas')
    
    if oferta.estado == 'cerrada':
        messages.error(request, 'No puedes editar una oferta cerrada.')
        return redirect('detalle_oferta', slug=slug)
    
    if request.method == 'POST':
        form = CrearOfertaLaboralForm(request.POST, instance=oferta)
        if form.is_valid():
            oferta_editada = form.save(commit=False)
            if oferta.estado == 'publicada':
                oferta_editada.estado = 'borrador'
                messages.info(request, 'La oferta ha vuelto a estado borrador debido a los cambios realizados.')
            oferta_editada.save()
            form.save_m2m()
            
            messages.success(request, 'Oferta editada exitosamente.')
            return redirect('detalle_oferta', slug=oferta_editada.slug)
    else:
        form = CrearOfertaLaboralForm(instance=oferta)
    
    context = {
        'form': form,
        'oferta': oferta,
        'titulo_pagina': f'Editar: {oferta.titulo}',
        'es_edicion': True
    }
    
    return render(request, 'usuarios/crear_oferta_laboral.html', context)


@login_required
def publicar_oferta_view(request, slug):
    """Vista para publicar una oferta (cambiar de borrador a publicada)"""
    oferta = get_object_or_404(OfertaLaboral, slug=slug)
    
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden publicar ofertas.')
        return redirect('inicio')
    
    if oferta.empleador != request.user.perfil_empleador:
        messages.error(request, 'No tienes permisos para publicar esta oferta.')
        return redirect('ver_mis_ofertas')
    
    if oferta.estado != 'borrador':
        messages.warning(request, 'Solo se pueden publicar ofertas en estado borrador.')
        return redirect('detalle_oferta', slug=slug)
    
    oferta.estado = 'publicada'
    oferta.save()
    
    messages.success(request, f'¡Oferta "{oferta.titulo}" publicada exitosamente!')
    return redirect('detalle_oferta', slug=slug)


@login_required
def cerrar_oferta_view(request, slug):
    """Vista para cerrar una oferta laboral"""
    oferta = get_object_or_404(OfertaLaboral, slug=slug)
    
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden cerrar ofertas.')
        return redirect('inicio')
    
    if oferta.empleador != request.user.perfil_empleador:
        messages.error(request, 'No tienes permisos para cerrar esta oferta.')
        return redirect('ver_mis_ofertas')
    
    if oferta.estado not in ['publicada', 'borrador']:
        messages.warning(request, 'Solo se pueden cerrar ofertas publicadas o en borrador.')
        return redirect('detalle_oferta', slug=slug)
    
    if request.method == 'POST':
        oferta.estado = 'cerrada'
        oferta.save()
        messages.success(request, f'Oferta "{oferta.titulo}" cerrada exitosamente.')
        return redirect('detalle_oferta', slug=slug)
    
    return render(request, 'usuarios/confirmar_cerrar_oferta.html', {
        'oferta': oferta,
        'titulo_pagina': f'Cerrar: {oferta.titulo}'
    })


@login_required
def reabrir_oferta_view(request, slug):
    """Vista para reabrir una oferta laboral cerrada"""
    oferta = get_object_or_404(OfertaLaboral, slug=slug)
    
    if request.user.tipo_usuario != 'empleador':
        messages.error(request, 'Solo los empleadores pueden reabrir ofertas.')
        return redirect('inicio')
    
    if oferta.empleador != request.user.perfil_empleador:
        messages.error(request, 'No tienes permisos para reabrir esta oferta.')
        return redirect('ver_mis_ofertas')
    
    if oferta.estado != 'cerrada':
        messages.warning(request, 'Solo se pueden reabrir ofertas cerradas.')
        return redirect('detalle_oferta', slug=slug)
    
    if request.method == 'POST':
        oferta.estado = 'publicada'
        oferta.save()
        messages.success(request, f'¡Oferta "{oferta.titulo}" reabierta exitosamente! Ahora está visible para músicos nuevamente.')
        return redirect('detalle_oferta', slug=slug)
    
    return render(request, 'usuarios/confirmar_reabrir_oferta.html', {
        'oferta': oferta,
        'titulo_pagina': f'Reabrir: {oferta.titulo}'
    })
