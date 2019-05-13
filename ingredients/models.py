from django.db import models


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=128)

    def __str__(self):
        return self.ingredient

