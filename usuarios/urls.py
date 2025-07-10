from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
