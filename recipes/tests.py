from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from recipes.constants import base64image
from users.models import UserProfile
from rest_framework.authtoken.models import Token
from recipes.models import Ingredient, Recipe


class BaseTestCase(TestCase):
    def create_user(self, username='testuser', email='testuser@mail.com'):
        user = UserProfile.objects.create_user(username=username, email=email, password='testuser_1')
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user, client


class ListCreateIngredientTestCase(BaseTestCase):
    url = reverse('list-create-ingredient')
    test_ingredient_name = 'test_ingredient'

    def create_ingredient(self, name, client):
        response = client.post(
            self.url,
            {'name': name, 'image': base64image},
        )
        return response

    def list_ingredient(self):
        client = APIClient()
        response = client.get(
            self.url,
        )
        return response

    def test_create_ingredient_with_user_authentication(self):
        user, client = self.create_user()
        response = self.create_ingredient(self.test_ingredient_name, client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), self.test_ingredient_name)
        self.assertIsNotNone(response.data.get('image'))

    def test_create_ingredient_without_user_authentication(self):
        client = APIClient()
        response = self.create_ingredient(self.test_ingredient_name, client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blank_ingredient(self):
        user, client = self.create_user()
        response = self.create_ingredient('', client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_name_ingredient(self):
        user_1, client_1 = self.create_user()
        response_1 = self.create_ingredient(self.test_ingredient_name, client_1)
        user_2, client_2 = self.create_user(username='testuser2', email='testuser2@mail.com')
        response_2 = self.create_ingredient(self.test_ingredient_name, client_2)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_1.data.get('name'), self.test_ingredient_name)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_ingredient(self):
        response = self.list_ingredient()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListCreateRecipeTestCase(BaseTestCase):
    url = reverse('list-create-recipe')

    def create_ingredients(self, name='test_ingredient'):
        ingredients = list()
        ingredient = Ingredient.objects.create(name=name, image=base64image)
        ingredients.append(ingredient.id)
        ingredient = Ingredient.objects.create(name='test_ingredient_2', image=base64image)
        ingredients.append(ingredient.id)
        return ingredients

    def create_recipe(self, client, ingredients, title='test_title', description='test_desc', difficulty='E', image=base64image):
        response = client.post(
            self.url,
            {
                'title': title, 'description': description, 'difficulty': difficulty,
                'ingredients': ingredients, 'image': image
            },
            format='json'
        )
        return response

    def list_recipes(self):
        client = APIClient()
        response = client.get(
            self.url,
        )
        return response

    def test_create_recipe_with_authentication(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client, ingredients)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('title'))
        self.assertIsNotNone(response.data.get('author'))
        self.assertIsNotNone(response.data.get('description'))
        self.assertIsNotNone(response.data.get('difficulty'))
        self.assertIsNotNone(response.data.get('image'))
        self.assertIsNotNone(response.data.get('ingredients'))

    def test_create_recipe_without_authentication(self):
        client = APIClient()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client, ingredients)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_without_title(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client=client, title=None, ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_description(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client=client, description=None, ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_difficulty(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client=client, difficulty=None, ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_incorrect_difficulty(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client=client, difficulty='A', ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_image(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        response = self.create_recipe(client=client, image='', ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('title'))
        self.assertIsNotNone(response.data.get('author'))
        self.assertIsNotNone(response.data.get('description'))
        self.assertIsNotNone(response.data.get('difficulty'))
        self.assertIsNotNone(response.data.get('ingredients'))

    def test_create_recipe_without_ingredients(self):
        user, client = self.create_user()
        ingredients = list()
        response = self.create_recipe(client=client, ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('title'))
        self.assertIsNotNone(response.data.get('author'))
        self.assertIsNotNone(response.data.get('description'))
        self.assertIsNotNone(response.data.get('difficulty'))
        self.assertIsNotNone(response.data.get('image'))

    def test_list_recipe(self):
        response = self.list_recipes()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RetrieveUpdateDestroyRecipeTestCase(BaseTestCase):
    def create_ingredients(self, any_update=False):
        ingredients = list()
        if not any_update:
            ingredient = Ingredient.objects.create(name='test_ingredient_1', image=base64image)
        else:
            ingredient = Ingredient.objects.create(name='test_ingredient_3', image=base64image)
        ingredients.append(ingredient.id)
        if not any_update:
            ingredient = Ingredient.objects.create(name='test_ingredient_2', image=base64image)
        else:
            ingredient = Ingredient.objects.create(name='test_ingredient_4', image=base64image)
        ingredients.append(ingredient.id)
        return ingredients

    def create_recipe(self, user):
        ingredients = self.create_ingredients()
        recipe = Recipe.objects.create(title='test_title', description='test_desc', difficulty='E', image=base64image, author=user)
        recipe.ingredients.add(ingredients[0])
        recipe.ingredients.add(ingredients[1])
        recipe.save()
        return recipe

    def test_author_can_update_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        ingredient = self.create_ingredients(any_update=True)
        response = client.put(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
            {
                'title': 'test', 'description': 'test', 'difficulty': 'E',
                'image': base64image, 'ingredients': ingredient
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_can_update_recipe(self):
        user_1, client_1 = self.create_user()
        user_2, client_2 = self.create_user(username='testuser2', email='testuser2@mail.com')
        recipe = self.create_recipe(user=user_1)
        ingredient = self.create_ingredients(any_update=True)
        response = client_2.put(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
            {
                'title': 'test', 'description': 'test', 'difficulty': 'E',
                'image': base64image, 'ingredients': ingredient
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_destroy_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        response = client.delete(
            reverse('recipe-detail', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_author_can_destroy_recipe(self):
        user_1, client_1 = self.create_user()
        user_2, client_2 = self.create_user(username='testuser2', email='testuser2@mail.com')
        recipe = self.create_recipe(user=user_1)
        response = client_2.delete(
            reverse('recipe-detail', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_retrieve_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        response = client.get(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_retrieve_recipe(self):
        user_1, client_1 = self.create_user()
        user_2, client_2 = self.create_user(username='testuser2', email='testuser2@mail.com')
        recipe = self.create_recipe(user=user_1)
        response = client_2.get(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
