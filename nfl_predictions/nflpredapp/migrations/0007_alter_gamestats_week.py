# Generated by Django 5.0.1 on 2024-01-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nflpredapp', '0006_gamestats_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestats',
            name='week',
            field=models.IntegerField(),
        ),
    ]
