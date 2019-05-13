from django.db import models

class Ingredients(models.Model):
    ingredient = models.CharField(max_length=128)