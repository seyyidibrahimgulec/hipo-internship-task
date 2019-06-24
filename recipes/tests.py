from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from recipes.constants import base64image
from users.models import UserProfile
from rest_framework.authtoken.models import Token
from recipes.models import Ingredient


class ListCreateIngredientTestCase(TestCase):
    url = reverse('list-create-ingredient')
    test_ingredient_name = 'test_ingredient'

    def create_user(self, username='testuser', email='testuser@mail.com'):
        user = UserProfile.objects.create_user(username=username, email=email, password='testuser_1')
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user, client

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


class ListCreateRecipeTestCase(TestCase):
    url = reverse('list-create-recipe')
    title = 'test_title'
    description = 'test_description'
    difficulty = 'E'

    def create_user(self, username='testuser', email='testuser@mail.com'):
        user = UserProfile.objects.create_user(username=username, email=email, password='testuser_1')
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user, client

    def create_ingredients(self, name='test_ingredient'):
        ingredients = list()
        ingredient = Ingredient.objects.create(name=name, image=base64image)
        ingredient.save()
        ingredients.append(ingredient.id)
        ingredient = Ingredient.objects.create(name='test_ingredient_2', image=base64image)
        ingredient.save()
        ingredients.append(ingredient.id)
        return ingredients

    def create_recipe(self, client, title='test_title', description='test_desc', difficulty='E', image=base64image, anyIngredients=True):
        if anyIngredients:
            ingredients = self.create_ingredients()
        else:
            ingredients = list()
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
        response = self.create_recipe(client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))

    def test_create_recipe_without_authentication(self):
        client = APIClient()
        response = self.create_recipe(client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_without_title(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, title=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_description(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, description=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_difficulty(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, difficulty=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_incorrect_difficulty(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, difficulty='A')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_image(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, image='')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))

    def test_create_recipe_without_ingredients(self):
        user, client = self.create_user()
        response = self.create_recipe(client=client, anyIngredients=False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_recipe(self):
        response = self.list_recipes()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
