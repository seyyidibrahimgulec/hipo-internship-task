from rest_framework import serializers
from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', )

    def create(self, validated_data):
        ingredient = Ingredient.objects.create(name=validated_data['name'])
        ingredient.save()
        return ingredient

