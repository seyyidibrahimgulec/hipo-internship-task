from django.db import models
from django.contrib.auth.models import User
from ingredients.models import Ingredient
from django.db.models import Avg


class Recipe(models.Model):
    DIFFICULTIES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    )

    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', help_text='(Hold down the Ctrl(Windows)/Command(Mac) button to select multiple options) ')

    def __str__(self):
        return self.title

    @property
    def rate_avg(self):
        rates = Rate.objects.filter(recipe=self.pk)
        ret_val = rates.aggregate(Avg('score'))['score__avg']
        if ret_val:
            return ret_val
        else:
            return 0

    @property
    def rate_count(self):
        count = Rate.objects.filter(recipe=self.pk).count()
        if count:
            return count
        else:
            return 0

    @property
    def like_count(self):
        count = Like.objects.filter(recipe=self.pk).count()
        if count:
            return count
        else:
            return 0


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.IntegerField()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

