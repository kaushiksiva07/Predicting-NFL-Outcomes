from django.db import models

class GameStats(models.Model):
    week = models.IntegerField() 
    home_team = models.CharField(max_length = 5)
    away_team = models.CharField(max_length = 5)
    ewma_dynamic_rush_off_home = models.FloatField()
    ewma_dynamic_pass_off_home = models.FloatField()
    ewma_dynamic_rush_def_home = models.FloatField()
    ewma_dynamic_pass_def_home = models.FloatField()
    ewma_dynamic_rush_off_away = models.FloatField()
    ewma_dynamic_pass_off_away = models.FloatField()
    ewma_dynamic_rush_def_away = models.FloatField()
    ewma_dynamic_pass_def_away = models.FloatField()

   