# Generated by Django 5.2.4 on 2025-08-01 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_observations'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type_order',
            field=models.CharField(choices=[('MAIL', 'Correios'), ('WHATSAPP', 'Whatsapp')], default='WHATSAPP', max_length=20, verbose_name='Tipo de Pedido'),
        ),
    ]
