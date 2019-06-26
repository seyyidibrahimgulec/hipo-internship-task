"""HipoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
# from recipes.views import (recipe_detail, index, NewRecipeView, like_recipe,
#                            rate_recipe, search, UpdateRecipeView, ingredient,
#                            DeleteRecipeView
#                            )
from django.urls import path
from recipes.views import ListCreateIngredientView, ListCreateRecipeView, RecipeDetailView, ListCreateDeleteLikesView
# from django.contrib.auth.decorators import login_required
from users.views import UserRegistrationView, UserAuthenticationView, MyProfileDetailView, ChangePasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profiles/create/', UserRegistrationView.as_view(), name='create-user'),
    path('api/profiles/authenticate/', UserAuthenticationView.as_view(), name='authenticate-user'),
    path('api/profiles/me/', MyProfileDetailView.as_view(), name='my-profile-detail'),
    path('api/profiles/me/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/ingredients/', ListCreateIngredientView.as_view(), name='list-create-ingredient'),
    path('api/recipes/', ListCreateRecipeView.as_view(), name='list-create-recipe'),
    path('api/recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('api/recipes/<int:pk>/likes/', ListCreateDeleteLikesView.as_view(), name='like-recipe'),
    # path('', index, name="index"),
    # path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('signup/', SignUp.as_view(), name='signup'),
    # path('search/', search, name='search'),
    # path('new_recipe/', login_required(NewRecipeView.as_view()), name='new_recipe'),
    # path('update_recipe/<int:pk>/', login_required(UpdateRecipeView.as_view()), name='update_recipe'),
    # path('delete_recipe/<int:pk>/', login_required(DeleteRecipeView.as_view()), name='delete_recipe'),
    # path('like_recipe/<int:pk>/', like_recipe, name="like_recipe"),
    # path('rate_recipe/<int:pk>/', rate_recipe, name="rate_recipe"),
    # path('ingredient/<str:ingredient_value>/', ingredient, name='ingredient'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
