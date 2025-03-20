from django.urls import path
from .views import alugar_carro, lista_carros, confirmar_aluguel, meus_alugueis, entregar_veiculo

urlpatterns = [
    path("", lista_carros, name="carros"),
    path("alugar/<int:carro_id>/", alugar_carro, name="alugar_carro"),
    path("confirmar_aluguel/<int:carro_id>/", confirmar_aluguel, name="confirmar_aluguel"),
    path("meus-alugueis/", meus_alugueis, name="meus_alugueis"),
    path("entregar-veiculo/<int:aluguel_id>/", entregar_veiculo, name="entregar_veiculo" ),
]
