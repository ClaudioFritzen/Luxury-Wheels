from django.urls import path
from carros.views import confirmar_aluguel
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('checkout/<int:aluguel_id>/', confirmar_aluguel, name='criar_sessao_pagamento'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cancelado/', views.cancelado, name='cancelado'),
    #path('webhook/', views.webhook, name='webhook'),

]