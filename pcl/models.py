from django.db import models

# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return(self.name)

    class Meta:
        ordering = ['name']

class Team(models.Model):
    name = models.CharField(max_length=200)
    division = models.ForeignKey(Division,
                                 on_delete=models.CASCADE)
    wins = models.FloatField(null=True, blank=True)
    losses = models.FloatField(null=True, blank=True)
    game_points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return(self.name)

    class Meta:
        ordering = ['name']


class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team,
                             on_delete=models.CASCADE)
    chessname = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    perf = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(self.name)

    class Meta:
        ordering = ['name']

