from django.contrib import admin
from .models import Ingredient, Recipe, Like, Rate, Image


admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Rate)
admin.site.register(Ingredient)
admin.site.register(Image)
