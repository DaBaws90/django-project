# Generated by Django 2.0.2 on 2019-01-24 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clientes', '0008_auto_20190124_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1, null=True, verbose_name='Género'),
        ),
    ]
