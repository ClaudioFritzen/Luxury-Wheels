
## Tabela para fazer as inspeções do carro
from datetime import timedelta
from django.db import models
from django.utils import timezone
from carros.models import Carro, Aluguel

from django.db.models.signals import post_save
from django.dispatch import receiver

class Inspecao(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='inspecoes')
    data_ultima_inspecao = models.DateField(default=timezone.now)
    data_proxima_revisao = models.DateField(default=timezone.now)
    data_proxima_inspecao_obrigatoria = models.DateField(default=timezone.now)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Aprovado", "Aprovado"),
            ("Reprovado", "Reprovado"),
            ("Pendente", "Pendente"),
        ],
        default="Pendente",
    )

    def atualizar_disponibilidade_veiculo(self):
        """
        Atualiza a disponibilidade do veículo considerando inspeções e aluguéis.
        """
        hoje = timezone.now().date()
        um_ano_atras = hoje - timedelta(days=365)

        # Verificar condições de inspeção
        if self.data_ultima_inspecao and self.data_ultima_inspecao < um_ano_atras:
            self.carro.disponibilidade = False
        elif self.data_proxima_revisao and self.data_proxima_revisao <= hoje:
            self.carro.disponibilidade = False

        # Adicionar lógica para aluguel ativo
        elif self.carro.aluguéis.filter(status="Ativo").exists():
            self.carro.disponibilidade = False
        else:
            self.carro.disponibilidade = True

        self.carro.save()

    class Meta:
        permissions = [
            ("pode_gerenciar_inspecoes", "Pode gerenciar inspeções"),
        ]

    def __str__(self):
        return f"Inspeção {self.id} - {self.carro.marca} {self.carro.modelo} - {self.status}"


## Funcao para atualizar a disponibilidade do carro após cada inspeção
# Sinal para atualizar disponibilidade do carro após salvar uma inspeção

@receiver(post_save, sender=Aluguel)
def atualizar_disponibilidade_apos_aluguel(sender, instance, **kwargs):
    """
    Atualiza a disponibilidade do veículo após salvar um aluguel.
    """
    if instance.status == "Ativo":
        instance.carro.disponibilidade = False
    elif instance.status in ["Finalizado", "Cancelado", "Concluido"]:
        instance.carro.disponibilidade = True

    instance.carro.save()

    print(f"Sinal chamado para aluguel {instance.id}")
    print(f"Disponibilidade do carro no sinal: {instance.carro.disponibilidade}")

class Relatorio(models.Model):
    # Campos do model

    class Meta:
        permissions = [
            ("ver_relatorios", "Pode visualizar relatórios"),
        ]
