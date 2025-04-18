from django.urls import path
from .views import alugar_carro, lista_carros, confirmar_aluguel, meus_alugueis, entregar_veiculo,extender_prazo,cancelar_aluguel

urlpatterns = [
    path("", lista_carros, name="carros"),
    path("alugar/<int:carro_id>/", alugar_carro, name="alugar_carro"),
    path("confirmar_aluguel/<int:carro_id>/", confirmar_aluguel, name="confirmar_aluguel"),
    path("meus-alugueis/", meus_alugueis, name="meus_alugueis"),
    path("entregar-veiculo/<int:aluguel_id>/", entregar_veiculo, name="entregar_veiculo" ),
    path("extender-prazo/<int:aluguel_id>/", extender_prazo, name="extender_prazo"),
    path("cancelar-reserva/<int:aluguel_id>/", cancelar_aluguel, name="cancelar_reserva"),
]
