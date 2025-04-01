from django.db import models
from carros.models import Carro
from django.utils import timezone

## Tabela para fazer as inspeções do carro
class Inspecao(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='inspecoes')
    data_ultima_inspecao = models.DateField(default=timezone.now)
    data_proxima_inspecao = models.DateField(default=timezone.now)
    data_proxima_inspecao_obrigatoria = models.DateField(default=timezone.now)  # Data da próxima inspeção obrigatória
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Aprovado", "Aprovado"),
            ("Reprovado", "Reprovado"),
            ("Pendente", "Pendente")
        ],
        default="Pendente"
        
    )

    class Meta:
        permissions = [
            ("pode_gerenciar_inspecoes", "Pode gerenciar inspeções"),
        ]
        

    def __str__(self):
        return f"Inspeção {self.id} - {self.carro} - {self.status}"

class Relatorio(models.Model):
    # Campos do model

    class Meta:
        permissions = [
            ("ver_relatorios", "Pode visualizar relatórios"),
        ]
