from django.urls import path
from . import views  # Importa as views do app gerenciamentos

urlpatterns = [
    path('relatorios/', views.relatorios, name='relatorio_alugueis'),  # URL para relatórios
]
