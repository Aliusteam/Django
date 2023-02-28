# Generated by Django 4.1.5 on 2023-01-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_movie_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='currency',
            field=models.CharField(choices=[('EUR', 'Euro'), ('USD', 'Dollar'), ('RUB', 'Rubles')], default='RUB', max_length=3),
        ),
    ]
