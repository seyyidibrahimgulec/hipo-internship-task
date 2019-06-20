from rest_framework.test import APIClient
from django.test import TestCase


class UserRegistrationTestCase(TestCase):
    def test_user_can_register(self):
        client = APIClient()
        response = client.post(
            '/api/profiles/create/',
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_existing_username_can_register(self):
        client = APIClient()
        response_user1 = client.post(
            '/api/profiles/create/',
            {'username': 'testuser', 'email': 'testuser1@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        response_user2 = client.post(
            '/api/profiles/create/',
            {'username': 'testuser', 'email': 'testuser2@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        self.assertEqual(response_user1.status_code, 201)
        self.assertEqual(response_user2.status_code, 400)

    def test_existing_email_can_register(self):
        client = APIClient()
        response_user1 = client.post(
            '/api/profiles/create/',
            {'username': 'testuser1', 'email': 'testuser@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        response_user2 = client.post(
            '/api/profiles/create/',
            {'username': 'testuser2', 'email': 'testuser@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        self.assertEqual(response_user1.status_code, 201)
        self.assertEqual(response_user2.status_code, 400)

    def test_short_password_can_register(self):
        client = APIClient()
        response = client.post(
            '/api/profiles/create/',
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'test'},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_entirely_numeric_password_can_register(self):
        client = APIClient()
        response = client.post(
            '/api/profiles/create/',
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': '12345678'},
            format='json'
        )
        self.assertEqual(response.status_code, 400)


class UserAuthenticationTestCase(TestCase):
    pass
