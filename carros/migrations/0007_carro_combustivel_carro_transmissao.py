# Generated by Django 5.1.6 on 2025-03-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0006_alter_aluguel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='carro',
            name='combustivel',
            field=models.CharField(choices=[('gasolina', 'Gasolina'), ('diesel', 'Diesel'), ('eletrico', 'Elétrico'), ('hibrido', 'Híbrido'), ('gpl', 'GPL')], default='gasolina', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carro',
            name='transmissao',
            field=models.CharField(choices=[('manual', 'Manual'), ('automatica', 'Automática')], default='manual', max_length=20),
            preserve_default=False,
        ),
    ]
