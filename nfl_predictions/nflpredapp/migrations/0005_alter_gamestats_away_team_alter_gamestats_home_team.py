# Generated by Django 5.0.1 on 2024-01-17 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nflpredapp', '0004_alter_gamestats_away_team_alter_gamestats_home_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestats',
            name='away_team',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='gamestats',
            name='home_team',
            field=models.CharField(max_length=5),
        ),
    ]