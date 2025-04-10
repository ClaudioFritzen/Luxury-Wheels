from datetime import timedelta
from django.db import models
from django.utils import timezone

# importando nosso usuario do app usuarios
from usuarios.models import Usuario

from .utils import calcular_dias_aluguel


# Create your models here.
class Carro(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    preco_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidade = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to="carros/imagens/", null=True, blank=True)

    TRANSMISSOES = [
        ('manual', 'Manual'),
        ('automatica', 'Automática'),
    ]

    COMBUSTIVEIS = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('eletrico', 'Elétrico'),
        ('hibrido', 'Híbrido'),
        ('gpl', 'GPL'),
    ]

    CATEGORIA = [
        ("pequeno", "Pequeno"),
        ("medio", "Médio"),
        ("grande", "Grande"),
        ("suv", "SUV"),
        ("luxo", "Luxo"),
    ]

    TIPO_VEICULOS = [
        ("carro", "Carro"),
        ("moto", "Moto"),
        ("motorhome", "MotorHome"),
    ]

    QTD_PESSOAS = [
        ("1-4", "1-4"),
        ("5-6", "5-6"),
        ("+7", "+7"),
    ]

    transmissao = models.CharField(max_length=20, choices=TRANSMISSOES, default='manual')
    combustivel = models.CharField(max_length=20, choices=COMBUSTIVEIS, default='gasolina')
    categoria = models.CharField(max_length=20, choices=CATEGORIA, default='medio')
    tipo_veiculos = models.CharField(max_length=20, choices=TIPO_VEICULOS, default='carro')
    qtd_pessoas = models.CharField(max_length=20, choices=QTD_PESSOAS, default='1-4')

    def atualizar_disponibilidade(self):
        """Atualiza a disponibilidade do carro com base nas inspeções e aluguéis ativos."""
        hoje = timezone.now().date()
        um_ano_atras = hoje - timedelta(days=365)

        # Verificar se há inspeções atrasadas
        for inspecao in self.inspecoes.all():
            if inspecao.data_ultima_inspecao and inspecao.data_ultima_inspecao < um_ano_atras:
                self.disponibilidade = False
                self.save()
                return
            elif inspecao.data_proxima_revisao and inspecao.data_proxima_revisao <= hoje:
                self.disponibilidade = False
                self.save()
                return

        # Verificar se há aluguéis ativos
        if self.aluguéis.filter(status="Ativo").exists():
            self.disponibilidade = False
        else:
            self.disponibilidade = True

        # Salvar a alteração no banco
        self.save()
        print(f"[DEBUG] Disponibilidade do carro ID {self.id} atualizada para {self.disponibilidade}")

    def __str__(self):
        return f"{self.marca} {self.modelo}"


## Parte do banco para salvar os carros alugados e fazer o calculo entre as datas
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Aluguel(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="aluguéis")
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="aluguéis")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Confirmado", "Confirmado"),
            ("Em Andamento", "Em Andamento"),
            ("Concluido", "Concluido"),
            ("Cancelado", "Cancelado"),
            ("Finalizado", "Finalizado"),
            ("Atrasado", "Atrasado"),
            ("Ativo", "Ativo"),
        ],
        default="Confirmado"
    )

    def calcula_preco_total(self):
        """Calculando o preço do tempo do veículo"""
        dias = calcular_dias_aluguel(self.data_inicio, self.data_fim)
        return self.carro.preco_diaria * dias if dias > 0 else self.carro.preco_diaria

    def save(self, *args, **kwargs):
        print(f"Salvando aluguel: {self.id}")
        print(f"Status do aluguel: {self.status}")
        print(f"Disponibilidade do carro antes: {self.carro.disponibilidade}")
        if self.status == "Ativo":
            self.carro.disponibilidade = False
        elif self.status in ["Finalizado", "Cancelado", "Concluido"]:
            self.carro.disponibilidade = True
        self.carro.save()
        print(f"Disponibilidade do carro depois: {self.carro.disponibilidade}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Aluguel de {self.carro} por {self.usuario} ({self.data_inicio} - {self.data_fim})"

    @property
    def dias(self):
        return (self.data_fim - self.data_inicio).days
