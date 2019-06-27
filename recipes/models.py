from django.db import models
from users.models import UserProfile
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTIES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    )

    title = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES, blank=False, null=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False, null=False)
    image = models.ImageField(null=True, blank=True)

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=False, help_text='(Hold down the Ctrl(Windows)/Command(Mac) button to select multiple options) ')

    def __str__(self):
        return self.title


class Rate(models.Model):
    user = models.ForeignKey(UserProfile, related_name='rates', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='rates', on_delete=models.CASCADE)
    score = models.IntegerField()


class Like(models.Model):
    user = models.ForeignKey(UserProfile, related_name='likes', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='likes', on_delete=models.CASCADE)
