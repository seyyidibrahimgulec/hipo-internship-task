from rest_framework import serializers
from recipes.models import Ingredient, Recipe
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'image')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    author = PresentablePrimaryKeyRelatedField(presentation_serializer=UserSerializer, read_only=True)
    ingredients = PresentablePrimaryKeyRelatedField(
        presentation_serializer=IngredientSerializer, queryset=Ingredient.objects.all(),
        many=True, allow_empty=False
    )
    average_rate = serializers.FloatField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    rate_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'title', 'description', 'difficulty',
            'image', 'ingredients', 'like_count', 'average_rate',
            'rate_count',
        )
