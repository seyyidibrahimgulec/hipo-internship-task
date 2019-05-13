from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    DIFFICULTIES = (
        ('E', 'EASY'),
        ('M', 'MEDIUM'),
        ('H', 'HARD'),
    )

    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # likes = models.ManyToManyField()
    # rates = models.ManyToManyField()
    # ingredients = models.ManyToManyField()