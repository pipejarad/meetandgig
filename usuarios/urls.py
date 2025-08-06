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
    path('portafolio/musico/editar/', views.editar_portafolio_musico, name='editar_portafolio_musico'),
    path('portafolio/<str:username>/', views.ver_portafolio_musico, name='ver_portafolio_musico'),
    
    # URLs del perfil público
    path('perfil/<str:username>/', views.ver_perfil_musico, name='ver_perfil_musico'),
]
