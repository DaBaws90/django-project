# Generated by Django 2.0.2 on 2019-01-28 21:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_restaurante', '0003_auto_20190126_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customerOrder', to='gestion_clientes.Customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weigth',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=2, max_digits=7)], verbose_name='Peso'),
        ),
    ]
