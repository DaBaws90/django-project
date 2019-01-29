# Generated by Django 2.0.2 on 2019-01-28 22:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_restaurante', '0004_auto_20190128_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weigth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Peso'),
        ),
    ]
