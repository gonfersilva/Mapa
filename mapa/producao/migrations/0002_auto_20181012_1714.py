# Generated by Django 2.0.7 on 2018-10-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bobine',
            name='estado',
            field=models.CharField(choices=[('G', 'G'), ('DM', 'DM12'), ('R', 'R'), ('BA', 'BA'), ('LAB', 'LAB'), ('IND', 'IND'), ('HOLD', 'HOLD')], default='G', max_length=4, verbose_name='Estado'),
        ),
    ]