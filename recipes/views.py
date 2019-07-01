# from django.shortcuts import render, redirect, reverse
# from recipes.models import Recipe, Like, Rate, Ingredient
# from django.core.paginator import Paginator
# from django.db.models import Count
# from django.views.generic import CreateView, UpdateView, DeleteView
# from recipes.forms import NewRecipesForm
# from django.contrib.auth.decorators import login_required
# from django.db.models.query import QuerySet
# from django.db.models import Q
# from recipes.permisions import SameUserOnlyPermission
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from recipes.serializers import IngredientSerializer, RecipeSerializer, ImageSerializer
from recipes.models import Ingredient, Recipe, Like, Rate
from rest_framework import permissions, status
from users.permisions import IsOwnerOrIsAdmin
from rest_framework.response import Response
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from users.models import UserProfile
from rest_framework.views import APIView
from django.db.models import Value, Avg, Count
from django.db.models.functions import Coalesce


class ListCreateIngredientView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing ingredients.

    post:
    Create a new ingredient instance.
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ListCreateRecipeView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing recipes.

    post:
    Create a new recipe instance.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().annotate(
        average_rate=Coalesce(Avg('rates__score'), Value(0)),
        like_count=Count('likes', distinct=True),
        rate_count=Count('rates', distinct=True),
    )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Return the given recipe.

    put:
    Update the given recipe.

    patch:
    Partial update the given recipe.

    delete:
    Delete the given recipe.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().annotate(
        average_rate=Coalesce(Avg('rates__score'), Value(0)),
        like_count=Count('likes', distinct=True),
        rate_count=Count('rates', distinct=True),
    )
    permission_classes = (IsOwnerOrIsAdmin, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ()
        return super(RecipeDetailView, self).get_permissions()


class ListCreateDeleteLikesView(ListAPIView):
    """
    get:
    Return the given recipe.

    post:
    Create a like for given recipe.

    delete:
    Delete the like for given recipe.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return get_object_or_404(Recipe.objects.all(), pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return UserProfile.objects.filter(likes__recipe=self.get_object()).distinct()

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        Like.objects.get_or_create(recipe=recipe, user=self.request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()
        Like.objects.filter(recipe=recipe, user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ()
        return super(ListCreateDeleteLikesView, self).get_permissions()


class CreateUpdateRatesView(APIView):
    """
    post:
    Create and Update rates for given recipe.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return get_object_or_404(Recipe.objects.all(), pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        Rate.objects.update_or_create(recipe=recipe, user=self.request.user, defaults={'score': self.request.data['score']})
        return Response(status=status.HTTP_200_OK)


class CreateImageView(CreateAPIView):
    """
    post:
    Create a new image instance.
    """
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )
