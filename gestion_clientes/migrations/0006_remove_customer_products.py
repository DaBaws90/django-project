# Generated by Django 2.0.2 on 2019-01-24 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clientes', '0005_auto_20190124_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='products',
        ),
    ]
