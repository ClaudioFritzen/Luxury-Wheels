# Generated by Django 5.1.6 on 2025-03-28 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamentos', '0002_transacao_mensagem_erro_transacao_metadados_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment Intent ID'),
        ),
    ]
