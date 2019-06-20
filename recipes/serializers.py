from rest_framework import serializers
from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('ingredient', )

    def create(self, validated_data):
        ingredient = Ingredient.objects.create(ingredient=validated_data['ingredient'])
        ingredient.save()
        return ingredient

