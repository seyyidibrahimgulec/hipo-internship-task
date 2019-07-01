from django.urls import path
from recipes.views import ListCreateIngredientView, ListCreateRecipeView, RecipeDetailView, \
    ListCreateDeleteLikesView, CreateUpdateRatesView, CreateImageView

urlpatterns = [
    path('api/ingredients/', ListCreateIngredientView.as_view(), name='list-create-ingredient'),
    path('api/recipes/', ListCreateRecipeView.as_view(), name='list-create-recipe'),
    path('api/recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('api/recipes/<int:pk>/likes/', ListCreateDeleteLikesView.as_view(), name='like-recipe'),
    path('api/recipes/<int:pk>/rates/', CreateUpdateRatesView.as_view(), name='rate-recipe'),
    path('api/images/', CreateImageView.as_view(), name='create-image'),
]
