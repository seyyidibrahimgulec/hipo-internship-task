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
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from recipes.serializers import IngredientSerializer, RecipeSerializer, ImageSerializer
from recipes.models import Ingredient, Recipe, Like, Rate, Image
from rest_framework import permissions, status
from users.permisions import IsOwnerOrIsAdmin
from rest_framework.response import Response
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from users.models import UserProfile
from rest_framework.views import APIView
from django.db.models import Value, Avg, Count
from django.db.models.functions import Coalesce

# class NewRecipeView(CreateView):
#     model = Recipe
#     form_class = NewRecipesForm
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.author = self.request.user
#         obj.save()
#         for ingredient in form.cleaned_data['ingredients']:
#             obj.ingredients.add(ingredient)
#
#         return redirect(recipe_detail, obj.id)
#
#
# class UpdateRecipeView(UpdateView, SameUserOnlyPermission):
#     model = Recipe
#     form_class = NewRecipesForm
#
#     # def form_valid(self, form):
#     #     obj = form.save(commit=True)
#     #     return redirect(recipe_detail, obj.id)
#
#     def get_success_url(self):
#         return reverse('recipe_detail', args=[self.kwargs['pk']])
#
#
# class DeleteRecipeView(DeleteView, SameUserOnlyPermission):
#     model = Recipe
#     template_name = 'recipes/recipe_confirm_delete.html'
#     success_url = '/'
#
#
# def main_page_view(request, all_recipes: QuerySet):
#     """
#     This is a not a standard django view function. This function used for main
#     page pagination and rendering functions. For instance search and index
#     page will show a very similar pages. But there is differences. This
#     function has the common operation in search, index and etc.
#     """
#     page_content_count = 2
#     paginator = Paginator(all_recipes, page_content_count)
#     page = request.GET.get('page')
#     recipes = paginator.get_page(page)
#
#     most_used_ingredients = Recipe.objects.all().values(
#         'ingredients__ingredient').annotate(
#             total=Count('ingredients')).order_by('-total')[:5]
#
#     context = {
#         "recipes": recipes,
#         "most_used_ingredients": most_used_ingredients
#     }
#
#     return render(request, "index.html", context)
#
#
# def index(request):
#     all_recipes = Recipe.objects.all().order_by('-created_time')
#     return main_page_view(request, all_recipes)
#
#
# def search(request):
#     terms = [x.strip() for x in request.GET.get("q").split(",")]
#     ids = set()
#     for term in terms:
#         for j in Ingredient.objects.filter(ingredient__contains=term):
#             ids.add(j.id)
#     result_recipes = Recipe.objects.filter(
#         ingredients__in=list(ids)).order_by("-created_time")
#     for term in terms:
#         tmp = Recipe.objects.filter(
#             Q(title__contains=term)
#             | Q(description__contains=term)).order_by('-created_time')
#         result_recipes = result_recipes | tmp
#
#     all_recipes = result_recipes.distinct()
#     return main_page_view(request, all_recipes)
#
#
# def ingredient(request, ingredient_value):
#     recipes = Recipe.objects.filter(ingredients__ingredient=ingredient_value)
#     return main_page_view(request, recipes)
#
#
# def recipe_detail(request, pk):
#     recipe = Recipe.objects.get(id=pk)
#     context = {
#         "recipe": recipe,
#     }
#
#     if request.user.is_authenticated:
#         like = Like.objects.filter(
#             user=request.user, recipe=recipe).first()
#
#         is_rated = Rate.objects.filter(
#             user=request.user, recipe=recipe).count()
#
#         rate_point = 0
#         if is_rated:
#             rate_point = Rate.objects.get(
#                 user=request.user, recipe=recipe).score
#
#         extra_context = {
#             "like": like,
#             "is_rated": is_rated,
#             "rate_point": rate_point,
#         }
#
#         context = {**context, **extra_context}
#
#     return render(request, 'recipe_detail.html', context)
#
#
# @login_required
# def like_recipe(request, pk):
#     recipe = Recipe.objects.get(pk=pk)
#     like, created = Like.objects.get_or_create(
#         user=request.user, recipe=recipe,
#     )
#     return redirect(recipe_detail, recipe.id)
#
#
# class DeleteLikeView(DeleteView):
#     model = Like
#     success_url = '/recipe/{recipe_id}/'
#
#
# @login_required
# def rate_recipe(request, pk):
#     recipe = Recipe.objects.get(id=pk)
#     rate_score = request.POST.get('score')
#     rate, created = Rate.objects.update_or_create(
#         user=request.user, recipe=recipe,
#         defaults={'score': rate_score},
#     )
#     return redirect(recipe_detail, recipe.id)


class ListCreateIngredientView(ListCreateAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ListCreateRecipeView(ListCreateAPIView):
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
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return get_object_or_404(Recipe.objects.all(), pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        Rate.objects.update_or_create(recipe=recipe, user=self.request.user, defaults={'score': self.request.data['score']})
        return Response(status=status.HTTP_200_OK)


class ListCreateImageView(ListCreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
