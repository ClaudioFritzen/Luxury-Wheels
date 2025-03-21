from django.db import models
from django.utils import timezone

# importando nosso usuario do app usuarios
from usuarios.models import Usuario


# Create your models here.
class Carro(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
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

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.ano}"


## Tabela para fazer as inspeções do carro
class Inspecao(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='inspecoes')
    data_inspecao = models.DateField(default=timezone.now)
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
    

## Parte do banco para salvar os carros alugados e fazer o calculo entre as datas
class Aluguel(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="aluguéis")
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="aluguéis")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Confirmado","Confirmado"),
            ("Em Andamento","Em Andamento"),
            ("Concluido","Concluido"),
            ("Cancelado","Cancelado"),
            ("Finalizado","Finalizado"),
            ("Atrasado","Atrasado"),
            ("Ativo", "Ativo"),
        ],
        default="Confirmado"
    )

    def calcula_preco_total(self):

        """Calculando o preço do tempo do veiclulo"""
        dias = (self.data_fim - self.data_inicio).days
        return self.carro.preco_diaria * dias if dias > 0 else self.carro.preco_diaria
    
    def save(self, *args, **kwargs):
        """Sobreescreve o save para calcular o preço antes de salvar"""
        self.preco_total = self.calcula_preco_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Aluguel de {self.carro} por {self.usuario} ({self.data_inicio} -{self.data_fim}"
