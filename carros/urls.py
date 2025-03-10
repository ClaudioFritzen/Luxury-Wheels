
from django.urls import path, include
from . import views

urlpatterns = [
   # path('usuarios/', include('usuarios.urls')),
   path("", views.lista_carros, name="carros")
]