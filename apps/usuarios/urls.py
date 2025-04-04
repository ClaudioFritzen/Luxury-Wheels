from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios/cadastro/", views.cadastro, name="cadastro"),
    path("usuarios/login/", views.logar, name="login"),  # Ajustado para chamar login_view
    path('logout/', views.logout_view, name='logout'),
    path('carros/', include('carros.urls')),
]
