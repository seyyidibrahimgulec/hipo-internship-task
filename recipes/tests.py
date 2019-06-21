from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from recipes.constants import base64image


class ListCreateIngredientTestCase(TestCase):
    url = reverse('list_create_ingredient')
    test_ingredient_name = 'test_ingredient'

    def create_ingredient(self, name):
        client = APIClient()
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

    def test_create_ingredient(self):
        response = self.create_ingredient(self.test_ingredient_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), self.test_ingredient_name)

    def test_blank_ingredient(self):
        response = self.create_ingredient('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_name_ingredient(self):
        response_1 = self.create_ingredient(self.test_ingredient_name)
        response_2 = self.create_ingredient(self.test_ingredient_name)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_1.data.get('name'), self.test_ingredient_name)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_ingredient(self):
        response = self.list_ingredient()
        self.assertEqual(response.status_code, status.HTTP_200_OK)



