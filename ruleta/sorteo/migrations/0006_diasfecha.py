# Generated by Django 4.1.7 on 2023-09-13 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0005_ruleta_terminos'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiasFecha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
            ],
        ),
    ]