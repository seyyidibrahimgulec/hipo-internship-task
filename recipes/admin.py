from django.contrib import admin
from .models import Recipe, Like, Rate


admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Rate)
