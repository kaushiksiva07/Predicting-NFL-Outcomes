# Generated by Django 5.0.1 on 2024-01-17 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nflpredapp', '0003_gamestats_away_team_gamestats_home_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestats',
            name='away_team',
            field=models.CharField(default=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='gamestats',
            name='home_team',
            field=models.CharField(default=True, max_length=3),
        ),
    ]
