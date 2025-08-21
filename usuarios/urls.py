from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("recuperar-password/", views.recuperar_password_view, name="recuperar_password"),
    path("cambiar-password/<uidb64>/<token>/", views.cambiar_password_view, name="cambiar_password"),
    path("perfil/musico/editar/", views.editar_perfil_musico, name="editar_perfil_musico"),
    path("perfil/musico/", views.ver_mi_perfil, name="ver_mi_perfil"),
    path('perfil-empleador/', views.perfil_empleador_view, name='perfil_empleador'),
    path('perfil-empleador/crear/', views.CrearPerfilEmpleadorView.as_view(), name='crear_perfil_empleador'),
    path('perfil-empleador/editar/', views.EditarPerfilEmpleadorView.as_view(), name='editar_perfil_empleador'),
    
    # URLs del portafolio
    path('portafolio/musico/', views.ver_mi_portafolio, name='ver_mi_portafolio'),
    path('portafolio/musico/crear/', views.editar_portafolio_musico, name='crear_portafolio_musico'),
    path('portafolio/musico/editar/', views.editar_portafolio_musico, name='editar_portafolio_musico'),
    
    # URL unificada del portafolio (público + privado)
    path('portafolio/<slug:slug>/', views.PortafolioUnificadoView.as_view(), name='ver_portafolio'),
    
    # URLs del perfil público
    path('perfil/<str:username>/', views.ver_perfil_musico, name='ver_perfil_musico'),
    
    # URLs de búsqueda (Ticket 2.8)
    path('buscar/', views.buscar_portafolios, name='buscar_portafolios'),
    path('musicos/', views.buscar_portafolios, name='listar_portafolios'),
    
    # URLs de ofertas laborales públicas (Ticket 3.2)
    path('ofertas/', views.buscar_ofertas_view, name='buscar_ofertas'),
    path('trabajos/', views.buscar_ofertas_view, name='listar_ofertas'),
    
    # URLs de ofertas laborales privadas (Sprint 3)
    path('ofertas/nueva/', views.crear_oferta_laboral_view, name='crear_oferta_laboral'),
    path('ofertas/mis-ofertas/', views.ver_mis_ofertas_view, name='ver_mis_ofertas'),
    path('ofertas/<slug:slug>/', views.detalle_oferta_view, name='detalle_oferta'),
    path('ofertas/<slug:slug>/editar/', views.editar_oferta_view, name='editar_oferta'),
    path('ofertas/<slug:slug>/publicar/', views.publicar_oferta_view, name='publicar_oferta'),
    path('ofertas/<slug:slug>/cerrar/', views.cerrar_oferta_view, name='cerrar_oferta'),
    path('ofertas/<slug:slug>/reabrir/', views.reabrir_oferta_view, name='reabrir_oferta'),
    path('ofertas/<slug:slug>/postular/', views.postular_oferta_view, name='postular_oferta'),
]
