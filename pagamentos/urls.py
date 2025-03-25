from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:aluguel_id>/', views.criar_sessao_pagamento, name='criar_sessao_pagamento'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cancelado/', views.cancelado, name='cancelado'),
    #path('webhook/', views.webhook, name='webhook'),

]