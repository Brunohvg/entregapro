# Generated by Django 5.2.4 on 2025-07-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_email_alter_customer_spent_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default=1, max_length=50, verbose_name='Celular'),
            preserve_default=False,
        ),
    ]
