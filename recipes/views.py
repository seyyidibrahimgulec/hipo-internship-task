from django.shortcuts import render
from recipes.models import Recipe, Like, Rate
from django.core.paginator import Paginator


def index(request):
    page_content_count = 1

    # Pagination
    all_recipes = Recipe.objects.all()
    paginator = Paginator(all_recipes, page_content_count)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    context = {
        'recipes': recipes,
    }

    return render(request, "index.html", context)


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    context = {
        "recipe": recipe,
    }

    if request.user:
        is_liked = Like.objects.filter(
            user=request.user, recipe=recipe).count()

        is_rated = Rate.objects.filter(
            user=request.user, recipe=recipe).count()

        rate_point = 0
        if is_rated:
            rate_point = Rate.objects.get(
                user=request.user, recipe=recipe).point

        extra_context = {
            "is_liked": is_liked,
            "is_rated": is_rated,
            "rate_point": rate_point,
        }

        context = {**context, **extra_context}

    return render(request, 'recipe_detail.html', context)


