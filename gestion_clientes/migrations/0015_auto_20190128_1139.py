# Generated by Django 2.0.2 on 2019-01-28 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clientes', '0014_auto_20190127_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='gestion_clientes.Customer', verbose_name='Escrito por'),
        ),
    ]
