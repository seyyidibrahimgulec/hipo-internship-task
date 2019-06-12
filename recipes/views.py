from django.shortcuts import render, redirect, reverse
from recipes.models import Recipe, Like, Rate, Ingredient
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import CreateView, UpdateView, DeleteView
from recipes.forms import NewRecipesForm
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.db.models import Q
from recipes.permisions import SameUserOnlyPermission


class NewRecipeView(CreateView):
    model = Recipe
    form_class = NewRecipesForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        for ingredient in form.cleaned_data['ingredients']:
            obj.ingredients.add(ingredient)

        return redirect(recipe_detail, obj.id)


class UpdateRecipeView(UpdateView, SameUserOnlyPermission):
    model = Recipe
    form_class = NewRecipesForm

    # def form_valid(self, form):
    #     obj = form.save(commit=True)
    #     return redirect(recipe_detail, obj.id)

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.kwargs['pk']])


class DeleteRecipeView(DeleteView, SameUserOnlyPermission):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = '/'


def main_page_view(request, all_recipes: QuerySet):
    """
    This is a not a standard django view function. This function used for main
    page pagination and rendering functions. For instance search and index
    page will show a very similar pages. But there is differences. This
    function has the common operation in search, index and etc.
    """
    page_content_count = 2
    paginator = Paginator(all_recipes, page_content_count)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    most_used_ingredients = Recipe.objects.all().values(
        'ingredients__ingredient').annotate(
            total=Count('ingredients')).order_by('-total')[:5]

    context = {
        "recipes": recipes,
        "most_used_ingredients": most_used_ingredients
    }

    return render(request, "index.html", context)


def index(request):
    all_recipes = Recipe.objects.all().order_by('-created_time')
    return main_page_view(request, all_recipes)


def search(request):
    terms = [x.strip() for x in request.GET.get("q").split(",")]
    ids = set()
    for term in terms:
        for j in Ingredient.objects.filter(ingredient__contains=term):
            ids.add(j.id)
    result_recipes = Recipe.objects.filter(
        ingredients__in=list(ids)).order_by("-created_time")
    for term in terms:
        tmp = Recipe.objects.filter(
            Q(title__contains=term)
            | Q(description__contains=term)).order_by('-created_time')
        result_recipes = result_recipes | tmp

    all_recipes = result_recipes.distinct()
    return main_page_view(request, all_recipes)


def ingredient(request, ingredient_value):
    recipes = Recipe.objects.filter(ingredients__ingredient=ingredient_value)
    return main_page_view(request, recipes)


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    context = {
        "recipe": recipe,
    }

    if request.user.is_authenticated:
        is_liked = Like.objects.filter(
            user=request.user, recipe=recipe).count()

        is_rated = Rate.objects.filter(
            user=request.user, recipe=recipe).count()

        rate_point = 0
        if is_rated:
            rate_point = Rate.objects.get(
                user=request.user, recipe=recipe).score

        extra_context = {
            "is_liked": is_liked,
            "is_rated": is_rated,
            "rate_point": rate_point,
        }

        context = {**context, **extra_context}

    return render(request, 'recipe_detail.html', context)


@login_required
def like_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)

    try:
        like = Like.objects.get(user=request.user, recipe=recipe)
        like.delete()
        return redirect(recipe_detail, recipe.id)

    except Like.DoesNotExist:
        Like.objects.create(user=request.user, recipe=recipe)
        return redirect(recipe_detail, recipe.id)


@login_required
def rate_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    rate_score = request.POST.get('score')
    rate, created = Rate.objects.update_or_create(
        user=request.user, recipe=recipe,
        defaults={'score': rate_score},
    )
    return redirect(recipe_detail, recipe.id)
