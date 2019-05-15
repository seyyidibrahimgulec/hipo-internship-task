from django import forms
from recipes.models import Recipe


class NewRecipes(forms.ModelForm):
    class Meta:
        model = Recipe

