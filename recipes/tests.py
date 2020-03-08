from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from recipes.constants import base64image
from users.models import UserProfile
from rest_framework.authtoken.models import Token
from recipes.models import Recipe, Like, Rate, RecipeImage, Ingredient, Image
import uuid
from drf_extra_fields.fields import Base64ImageField


class BaseTestCase(TestCase):
    def create_user(self):
        username = f"test_user_{str(uuid.uuid4())}"
        email = f"{username}@mail.com"
        password = f"{username}{str(uuid.uuid4())}"
        user = UserProfile.objects.create_user(username=username, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user, client

    def create_ingredients(self, ingredient_quantity=2):
        ingredient_ids = list()
        for i in range(ingredient_quantity):
            name = f"test_ingredient_{str(uuid.uuid4())}"
            image = Base64ImageField().to_internal_value(base64image)
            ingredient_ids.append(Ingredient.objects.create(name=name, image=image).id)
        return ingredient_ids

    def create_admin(self):
        username = f"test_user_{str(uuid.uuid4())}"
        email = f"{username}@mail.com"
        password = f"{username}{str(uuid.uuid4())}"
        user = UserProfile.objects.create_superuser(username=username, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user, client

    def create_recipe(self, user):
        ingredients = self.create_ingredients()
        recipe = Recipe.objects.create(title='test_title', description='test_desc', difficulty='E', author=user)
        image_file = Base64ImageField().to_internal_value(base64image)
        image = Image.objects.create(image=image_file)
        RecipeImage.objects.create(recipe=recipe, image=image)
        RecipeImage.objects.create(recipe=recipe, image=image)
        recipe.ingredients.add(ingredients[0])
        recipe.ingredients.add(ingredients[1])
        return recipe

    def create_images(self):
        image_ids = list()
        for i in range(2):
            image_file = Base64ImageField().to_internal_value(base64image)
            image = Image.objects.create(image=image_file)
            image_ids.append(image.id)
        return image_ids


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
        user_2, client_2 = self.create_user()
        response_2 = self.create_ingredient(self.test_ingredient_name, client_2)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_1.data.get('name'), self.test_ingredient_name)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_ingredient(self):
        response = self.list_ingredient()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListCreateRecipeTestCase(BaseTestCase):
    url = reverse('list-create-recipe')

    def create_recipe(self, client, ingredients, images, title='test_title', description='test_desc', difficulty='E'):
        response = client.post(
            self.url,
            {
                'title': title, 'description': description, 'difficulty': difficulty,
                'ingredients': ingredients, 'images': images
            },
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
        images = self.create_images()
        response = self.create_recipe(client, ingredients, images)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('author').get('username'), user.username)
        self.assertEqual([d['id'] for d in response.data.get('images')], images)
        self.assertEqual([d['id'] for d in response.data.get('ingredients')], ingredients)

    def test_create_recipe_without_authentication(self):
        client = APIClient()
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = self.create_recipe(client, ingredients, images)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_without_title(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = self.create_recipe(client=client, title='', ingredients=ingredients, images=images)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_description(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = self.create_recipe(client=client, description='', ingredients=ingredients, images=images)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_difficulty(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = self.create_recipe(client=client, difficulty='', ingredients=ingredients, images=images)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_incorrect_difficulty(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = self.create_recipe(client=client, difficulty='A', ingredients=ingredients, images=images)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_image(self):
        user, client = self.create_user()
        ingredients = self.create_ingredients()
        images = list()
        response = self.create_recipe(client=client, images=images, ingredients=ingredients)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_ingredients(self):
        user, client = self.create_user()
        ingredients = list()
        images = self.create_images()
        response = self.create_recipe(client=client, ingredients=ingredients, images=images)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_recipe(self):
        response = self.list_recipes()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RetrieveUpdateDestroyRecipeTestCase(BaseTestCase):
    def test_author_can_update_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        ingredients = self.create_ingredients()
        images = self.create_images()
        update_title = 'update_title'
        update_description = 'update_description'
        update_difficulty = 'E'
        response = client.put(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
            {
                'title': update_title, 'description': update_description, 'difficulty': update_difficulty,
                'images': images, 'ingredients': ingredients
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('author').get('username'), user.username)
        self.assertEqual([d['id'] for d in response.data.get('ingredients')], ingredients)
        self.assertEqual([d['id'] for d in response.data.get('images')], images)
        self.assertEqual(response.data.get('title'), update_title)
        self.assertEqual(response.data.get('description'), update_description)
        self.assertEqual(response.data.get('difficulty'), update_difficulty)

    def test_non_author_can_update_recipe(self):
        user_1, client_1 = self.create_user()
        user_2, client_2 = self.create_user()
        recipe = self.create_recipe(user=user_1)
        ingredients = self.create_ingredients()
        images = self.create_images()
        update_title = 'update_title'
        update_description = 'update_description'
        update_difficulty = 'E'
        response = client_2.put(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
            {
                'title': update_title, 'description': update_description, 'difficulty': update_difficulty,
                'images': images, 'ingredients': ingredients
            },
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
        user_2, client_2 = self.create_user()
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
        user_2, client_2 = self.create_user()
        recipe = self.create_recipe(user=user_1)
        response = client_2.get(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_recipe(self):
        user, client = self.create_user()
        admin_user, admin_client = self.create_admin()
        recipe = self.create_recipe(user=user)
        update_title = 'update_title'
        update_description = 'update_description'
        update_difficulty = 'E'
        ingredients = self.create_ingredients()
        images = self.create_images()
        response = admin_client.put(
            reverse('recipe-detail', kwargs={'pk': recipe.id}),
            {
                'title': update_title, 'description': update_description, 'difficulty': update_difficulty,
                'images': images, 'ingredients': ingredients
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('author').get('username'), user.username)
        self.assertEqual([d['id'] for d in response.data.get('ingredients')], ingredients)
        self.assertEqual([d['id'] for d in response.data.get('images')], images)
        self.assertEqual(response.data.get('title'), update_title)
        self.assertEqual(response.data.get('description'), update_description)
        self.assertEqual(response.data.get('difficulty'), update_difficulty)

    def test_admin_can_destroy_recipe(self):
        user, client = self.create_user()
        admin_user, admin_client = self.create_admin()
        recipe = self.create_recipe(user=user)
        response = admin_client.delete(
            reverse('recipe-detail', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ListCreateDeleteLikesTestCase(BaseTestCase):
    def test_user_can_like_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        response = client.post(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(recipe.likes.first())
        self.assertEqual(user, recipe.likes.first().user)

    def test_non_user_can_like_recipe(self):
        user, user_client = self.create_user()
        client = APIClient()
        recipe = self.create_recipe(user=user)
        response = client.post(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_list_like_of_recipes(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        response = client.get(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_user_can_list_like_of_recipes(self):
        user, user_client = self.create_user()
        client = APIClient()
        recipe = self.create_recipe(user=user)
        response = client.get(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_unlike_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        Like.objects.create(user=user, recipe=recipe)
        response = client.delete(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(recipe.likes.first())
        response = client.delete(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_user_unlike_recipe(self):
        user, user_client = self.create_user()
        client = APIClient()
        recipe = self.create_recipe(user=user)
        Like.objects.create(user=user, recipe=recipe)
        response = client.delete(
            reverse('like-recipe', kwargs={'pk': recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_count(self):
        user_1, user_1_client = self.create_user()
        user_2, user_2_client = self.create_user()
        recipe = self.create_recipe(user=user_1)
        Like.objects.create(user=user_1, recipe=recipe)
        response = user_1_client.get(
            reverse('list-create-recipe')
        )
        self.assertEqual(response.data['results'][0]['like_count'], 1)
        response = user_1_client.get(
            reverse('recipe-detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.data['like_count'], 1)
        Like.objects.create(user=user_2, recipe=recipe)
        response = user_1_client.get(
            reverse('list-create-recipe')
        )
        self.assertEqual(response.data['results'][0]['like_count'], 2)
        response = user_1_client.get(
            reverse('recipe-detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.data['like_count'], 2)


class CreateUpdateRatesTestCase(BaseTestCase):
    def test_can_user_create_rate_to_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        score = 5
        response = client.post(
            reverse('rate-recipe', kwargs={'pk': recipe.id}),
            {'score': score}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Rate.objects.filter(user=user, recipe=recipe, score=score).exists())

    def test_can_non_user_create_rate_to_recipe(self):
        user, user_client = self.create_user()
        client = APIClient()
        recipe = self.create_recipe(user=user)
        score = 5
        response = client.post(
            reverse('rate-recipe', kwargs={'pk': recipe.id}),
            {'score': score}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_user_update_rate_to_recipe(self):
        user, client = self.create_user()
        recipe = self.create_recipe(user=user)
        old_score = 5
        new_score = 3
        Rate.objects.create(recipe=recipe, user=user, score=old_score)
        response = client.post(
            reverse('rate-recipe', kwargs={'pk': recipe.id}),
            {'score': new_score}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Rate.objects.filter(user=user, recipe=recipe, score=new_score).exists())

    def test_can_non_user_update_rate_to_recipe(self):
        user, user_client = self.create_user()
        client = APIClient()
        recipe = self.create_recipe(user=user)
        old_score = 5
        new_score = 3
        Rate.objects.create(recipe=recipe, user=user, score=old_score)
        response = client.post(
            reverse('rate-recipe', kwargs={'pk': recipe.id}),
            {'score': new_score}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_user_update_other_users_rate(self):
        user_a, user_a_client = self.create_user()
        user_b, user_b_client = self.create_user()
        recipe = self.create_recipe(user=user_a)
        old_score = 5
        new_score = 3
        Rate.objects.create(recipe=recipe, user=user_a, score=old_score)
        user_b_client.post(
            reverse('rate-recipe', kwargs={'pk': recipe.id}),
            {'score': new_score}
        )
        self.assertEqual(Rate.objects.get(user=user_a, recipe=recipe).score, old_score)

    def test_rate_count_and_average_rate(self):
        user_1, user_1_client = self.create_user()
        user_2, user_2_client = self.create_user()
        recipe = self.create_recipe(user=user_1)
        score_1 = 4
        score_2 = 2
        average = (score_1 + score_2) / 2
        Rate.objects.create(user=user_1, recipe=recipe, score=score_1)
        response = user_1_client.get(
            reverse('list-create-recipe')
        )
        self.assertEqual(response.data['results'][0]['rate_count'], 1)
        self.assertEqual(response.data['results'][0]['average_rate'], score_1)
        response = user_1_client.get(
            reverse('recipe-detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.data['rate_count'], 1)
        self.assertEqual(response.data['average_rate'], score_1)
        Rate.objects.create(user=user_2, recipe=recipe, score=score_2)
        response = user_1_client.get(
            reverse('list-create-recipe')
        )
        self.assertEqual(response.data['results'][0]['rate_count'], 2)
        self.assertEqual(response.data['results'][0]['average_rate'], average)
        response = user_1_client.get(
            reverse('recipe-detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.data['rate_count'], 2)
        self.assertEqual(response.data['average_rate'], average)


class CreateImageTestCase(BaseTestCase):
    url = reverse('create-image')

    def test_user_can_create_image(self):
        user, client = self.create_user()
        response = client.post(
            self.url,
            {'image': base64image}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['image'])

    def test_non_user_can_create_image(self):
        client = APIClient()
        response = client.post(
            self.url,
            {'image': base64image}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_temp(self):
        self.assertFalse(True)
