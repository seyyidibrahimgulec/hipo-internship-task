from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from recipes.constants import base64image
from users.models import UserProfile
from rest_framework.authtoken.models import Token


class ListCreateIngredientTestCase(TestCase):
    url = reverse('list-create-ingredient')
    test_ingredient_name = 'test_ingredient'

    def create_ingredient(self, name, fail_authenticate=False, username='testuser', email='testuser@mail.com'):
        user = UserProfile.objects.create_user(username=username, email=email, password='testuser_1')
        token, created = Token.objects.get_or_create(user=user)
        client = APIClient()
        if not fail_authenticate:
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key + 'fail')
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
        response = self.create_ingredient(self.test_ingredient_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), self.test_ingredient_name)
        self.assertIsNotNone(response.data.get('image'))

    def test_create_ingredient_without_user_authentication(self):
        response = self.create_ingredient(self.test_ingredient_name, fail_authenticate=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blank_ingredient(self):
        response = self.create_ingredient('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_name_ingredient(self):
        response_1 = self.create_ingredient(self.test_ingredient_name)
        response_2 = self.create_ingredient(self.test_ingredient_name, username='testuser2', email='testuser2@mail.com')
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_1.data.get('name'), self.test_ingredient_name)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_ingredient(self):
        response = self.list_ingredient()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
