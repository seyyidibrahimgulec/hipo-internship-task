from django.contrib import admin
from .models import Recipe, Like, Rate, Ingredient


admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Rate)
admin.site.register(Ingredient)
