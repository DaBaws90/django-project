# Generated by Django 2.0.2 on 2019-01-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clientes', '0004_auto_20190119_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Foto'),
        ),
    ]
