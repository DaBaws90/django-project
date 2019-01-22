# Generated by Django 2.0.2 on 2019-01-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_restaurante', '0002_auto_20190122_0934'),
        ('gestion_clientes', '0003_remove_customer_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='products',
            field=models.ManyToManyField(through='gestion_restaurante.Order', to='gestion_restaurante.Product'),
        ),
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(default=None),
            preserve_default=False,
        ),
    ]
