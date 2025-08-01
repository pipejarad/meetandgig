from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("recuperar-password/", views.recuperar_password_view, name="recuperar_password"),
    path("cambiar-password/<uidb64>/<token>/", views.cambiar_password_view, name="cambiar_password"),
]
