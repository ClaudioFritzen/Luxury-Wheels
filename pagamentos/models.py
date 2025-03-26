from django.db import models
from carros.models import Aluguel

from django.db import models
from django.db.models import JSONField

class Transacao(models.Model):
    PENDENTE = "pendente"
    SUCESSO = "sucesso"
    FALHA = "falha"

    STATUS_CHOICES = [
        (PENDENTE, "Pendente"),
        (SUCESSO, "Sucesso"),
        (FALHA, "Falha"),
    ]

    aluguel = models.ForeignKey(Aluguel, on_delete=models.CASCADE, related_name="transacoes")
    stripe_id = models.CharField(max_length=255, blank=True, null=True)  # Stripe ID opcional
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDENTE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    mensagem_erro = models.TextField(blank=True, null=True)  # Armazena mensagens de erro do Stripe
    metadados = JSONField(blank=True, null=True)  # Armazena informações dinâmicas do Stripe

    def save(self, *args, **kwargs):
        if self.valor <= 0:
            raise ValueError("O valor da transação deve ser maior que zero.")
        if self.status == self.SUCESSO and not self.stripe_id:
            raise ValueError("Transações com status 'sucesso' devem conter um 'stripe_id'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transação {self.stripe_id or 'N/A'} - {self.status} - {self.valor}€ em {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["aluguel"]),
        ]
