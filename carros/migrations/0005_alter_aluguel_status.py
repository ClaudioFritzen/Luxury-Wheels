# Generated by Django 5.1.6 on 2025-03-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0004_aluguel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluguel',
            name='status',
            field=models.CharField(choices=[('Confirmado', 'Confirmado'), ('Em Andamento', 'Em Andamento'), ('Concluido', 'Concluido'), ('Cancelado', 'Cancelado'), ('Finalizado', 'Finalizado'), ('Atrasado', 'Atrasado')], default='Confirmado', max_length=20),
        ),
    ]
