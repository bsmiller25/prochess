from django.db import models

# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=200)

class Team(models.Model):
    name = models.CharField(max_length=200)
    division = models.ForeignKey(Division,
                                 on_delete=models.CASCADE)
    wins = models.FloatField(null=True, blank=True)
    losses = models.FloatField(null=True, blank=True)
    game_points = models.FloatField(null=True, blank=True)

class Player(models.Model):
    name = models.CharField(max_length=200)
    chessname = models.CharField(max_length=200)
    rating = models.IntegerField(null=True, blank=True)
    perf = models.IntegerField(null=True, blank=True)
   