from django.db import models


class Superhero(models.Model):
    name = models.CharField(max_length=100, unique=True)
    intelligence = models.IntegerField()
    strength = models.IntegerField()
    speed = models.IntegerField()
    power = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name