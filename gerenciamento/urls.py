from django.urls import path
from gerenciamento.views import relatorios,lista_inspecoes, nova_inspecao, editar_inspecao, excluir_inspecao
urlpatterns = [
    path('relatorios/', relatorios, name='relatorio_alugueis'),  # URL para relatórios
    path('<int:carro_id>/inspecoes/', lista_inspecoes, name='lista_inspecoes'),
    path('<int:carro_id>/inspecoes/nova/', nova_inspecao, name='nova_inspecao'),
    path('<int:inspecao_id>/editar/', editar_inspecao, name='editar_inspecao'),
    path('<int:inspecao_id>/excluir/', excluir_inspecao, name='excluir_inspecao'),


]
