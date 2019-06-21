from rest_framework import serializers
from recipes.models import Ingredient
from drf_extra_fields.fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'image')
