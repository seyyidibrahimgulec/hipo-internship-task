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
from recipes.views import recipe_detail, index, NewRecipe, like_recipe, rate_recipe
from django.urls import path, include
from users.views import SignUp


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('recipe/<int:pk>/', recipe_detail),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    path('new_recipe/', NewRecipe.as_view(), name='new_recipe'),
    path('like_recipe/<int:pk>/', like_recipe, name="like_recipe"),
    path('rate_recipe/<int:pk>/', rate_recipe, name="rate_recipe"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
