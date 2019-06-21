from rest_framework import serializers
from recipes.models import Ingredient
from drf_extra_fields.fields import Base64ImageField
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy


class IngredientSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    image = Base64ImageField(required=False)

    def create(self, validated_data):
        try:
            ingredient = Ingredient(name=validated_data['name'], image=validated_data['image'])
            ingredient.save()
            return ingredient
        except IntegrityError:
            msg = ugettext_lazy('The ingredient you have entered is already exist.')
            raise serializers.ValidationError(msg)
