from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status


class CreateIngredientTestCase(TestCase):
    url = reverse('create_ingredient')

    def create_response(self, name):
        client = APIClient()
        response = client.post(
            self.url,
            {'name': name},
            format='json'
        )
        return name, response

    def test_create_ingredient(self):
        name, response = self.create_response('test_ingredient')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'test_ingredient')

    def test_blank_ingredient(self):
        ingredient, response = self.create_response('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_ingredient(self):
        ingredient, response = self.create_response(None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListIngredientTestCase(TestCase):
    url = reverse('list_ingredient')

    def create_response(self):
        client = APIClient()
        response = client.get(
            self.url,
            format='json'
        )
        return response

    def test_list_ingredient(self):
        response = self.create_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
