# Generated by Django 5.1.6 on 2025-03-25 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0009_alter_inspecao_options'),
        ('pagamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='mensagem_erro',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transacao',
            name='metadados',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='aluguel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to='carros.aluguel'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('sucesso', 'Sucesso'), ('falha', 'Falha')], default='pendente', max_length=50),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddIndex(
            model_name='transacao',
            index=models.Index(fields=['status'], name='pagamentos__status_b6c374_idx'),
        ),
        migrations.AddIndex(
            model_name='transacao',
            index=models.Index(fields=['aluguel'], name='pagamentos__aluguel_3775ba_idx'),
        ),
    ]
