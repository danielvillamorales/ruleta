# Generated by Django 4.1.7 on 2023-04-24 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0002_ruleta_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleta',
            name='porcentaje',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
