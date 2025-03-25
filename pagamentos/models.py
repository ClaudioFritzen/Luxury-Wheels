from django.db import models
from carros.models import Aluguel

class Transacao(models.Model):
    aluguel = models.OneToOneField(Aluguel, on_delete=models.CASCADE, related_name="transacao")
    stripe_id = models.CharField(max_length=255)  # ID único da transação gerado pelo Stripe
    status = models.CharField(
        max_length=50,
        choices=[
            ("sucesso", "Sucesso"),
            ("falha", "Falha"),
            ("pendente", "Pendente"),
        ],
        default="pendente"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transação {self.stripe_id} - {self.status}"
