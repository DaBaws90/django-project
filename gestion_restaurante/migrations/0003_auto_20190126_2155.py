# Generated by Django 2.0.2 on 2019-01-26 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_restaurante', '0002_auto_20190124_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha'),
        ),
    ]
