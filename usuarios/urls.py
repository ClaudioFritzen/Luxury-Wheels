from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    
]
