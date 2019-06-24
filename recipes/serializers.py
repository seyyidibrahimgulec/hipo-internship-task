from rest_framework import serializers
from recipes.models import Ingredient, Recipe
from drf_extra_fields.fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'image')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'title', 'description', 'difficulty',
            'image', 'ingredients'
        )
