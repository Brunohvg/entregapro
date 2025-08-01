# Generated by Django 5.2.4 on 2025-07-25 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('PENDING', 'Aguardando coleta'), ('PICKED_UP', 'Coletado pelo motoboy'), ('ON_THE_WAY', 'Em rota de entrega'), ('DELIVERED', 'Entregue ao destinatário'), ('FAILED', 'Entrega não realizada'), ('RETURNED', 'Pedido devolvido ao remetente'), ('CANCELLED', 'Entrega cancelada')], default='PENDING', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Aguardando pagamento'), ('PAID', 'Pagamento aprovado'), ('REFUSED', 'Pagamento recusado')], default='PENDING', max_length=20, verbose_name='Status Pagamento'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nº Pedido'),
        ),
    ]
