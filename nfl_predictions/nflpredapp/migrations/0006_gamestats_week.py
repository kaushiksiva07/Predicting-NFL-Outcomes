# Generated by Django 5.0.1 on 2024-01-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nflpredapp', '0005_alter_gamestats_away_team_alter_gamestats_home_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamestats',
            name='week',
            field=models.IntegerField(default=0),
        ),
    ]