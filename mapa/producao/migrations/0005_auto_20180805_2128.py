# Generated by Django 2.0.7 on 2018-08-05 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producao', '0004_perfil_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='produto',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Produto'),
        ),
    ]
