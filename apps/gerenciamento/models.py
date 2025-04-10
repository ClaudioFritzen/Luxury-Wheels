from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from carros.models import Carro
from django.utils import timezone

## Tabela para fazer as inspeções do carro
class Inspecao(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='inspecoes')
    data_ultima_inspecao = models.DateField(default=timezone.now)
    data_proxima_revisao = models.DateField(default=timezone.now)
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

    def verificar_disponibilidade_revisao(self):
        
        hoje = timezone.now().date()
        um_ano_atras = hoje - timezone.timedelta(days=365)

        if self.data_ultima_inspecao and self.data_ultima_inspecao < um_ano_atras:
            self.carro.disponibilidade = False
            print(f"Inspeção {self.id}: indisponível devido à última inspeção.")
        elif self.data_proxima_revisao and self.data_proxima_revisao <= hoje:
            self.carro.disponibilidade = False
            print(f"Inspeção {self.id}: indisponível devido à próxima revisão.")
        else:
            self.carro.disponibilidade = True
            print(f"Inspeção {self.id}: disponível.")

        self.carro.save()


    class Meta:
        permissions = [
            ("pode_gerenciar_inspecoes", "Pode gerenciar inspeções"),
        ]
        

    def __str__(self):
        return f"Inspeção {self.id} - {self.carro} - {self.status}"

## Funcao para atualizar a disponibilidade do carro após cada inspeção
# Sinal para atualizar disponibilidade do carro após salvar uma inspeção

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Inspecao)
def atualizar_disponibilidade_veiculo(sender, instance, **kwargs):
    hoje = timezone.now().date()
    um_ano_atras = hoje - timedelta(days=365)

    # Verificar disponibilidade
    if instance.data_ultima_inspecao and instance.data_ultima_inspecao < um_ano_atras:
        instance.carro.disponibilidade = False
    elif instance.data_proxima_revisao and instance.data_proxima_revisao <= hoje:
        instance.carro.disponibilidade = False
    else:
        instance.carro.disponibilidade = True

    # Salvar alterações no carro
    instance.carro.save()

class Relatorio(models.Model):
    # Campos do model

    class Meta:
        permissions = [
            ("ver_relatorios", "Pode visualizar relatórios"),
        ]
