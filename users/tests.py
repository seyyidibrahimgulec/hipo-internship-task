from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework.authtoken.models import Token
from users.models import UserProfile
from django.urls import reverse


class UserRegistrationTestCase(TestCase):
    url = reverse('create_user')

    def test_user_can_register(self):
        client = APIClient()
        response = client.post(
            self.url,
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('username'), 'testuser')
        self.assertEqual(response.data.get('email'), 'testuser@mail.com')

    def test_existing_username_can_register(self):
        client = APIClient()
        response_user1 = client.post(
            self.url,
            {'username': 'testuser', 'email': 'testuser1@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        response_user2 = client.post(
            self.url,
            {'username': 'testuser', 'email': 'testuser2@mail.com', 'password': 'testuser_1'},
            format='json'
        )
        self.assertEqual(response_user1.status_code, 201)
        self.assertEqual(response_user1.data.get('username'), 'testuser')
        self.assertEqual(response_user1.data.get('email'), 'testuser1@mail.com')
        self.assertEqual(response_user2.status_code, 400)

    def test_existing_email_can_register(self):
        client = APIClient()
        response_user1 = client.post(
            self.url,
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
            self.url,
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'test'},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_entirely_numeric_password_can_register(self):
        client = APIClient()
        response = client.post(
            self.url,
            {'username': 'testuser', 'email': 'testuser@mail.com', 'password': '12345678'},
            format='json'
        )
        self.assertEqual(response.status_code, 400)


class UserAuthenticationTestCase(TestCase):
    url = reverse('authenticate_user')
    params = {
        'username': 'testuser',
        'email': 'testuser@mail.com',
        'password': 'testuser_1'
    }

    def create_user_and_response(self, email, password):
        client = APIClient()
        user = UserProfile.objects.create(username=self.params['username'], email=self.params['email'])
        user.set_password(self.params['password'])
        user.save()
        response = client.post(
            self.url,
            {'email': email, 'password': password},
            format='json'
        )
        return user, response

    def test_user_can_authenticate(self):
        user, response = self.create_user_and_response(self.params['email'], self.params['password'])
        token = Token.objects.get(user=user)
        self.assertEqual(response.data.get('token'), token.key)
        self.assertEqual(response.data.get('username'), user.username)
        self.assertEqual(response.status_code, 200)

    def test_incorrect_email_can_authenticate(self):
        user, response = self.create_user_and_response('testuser@email.com', self.params['password'])
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_can_authenticate(self):
        user, response = self.create_user_and_response('testuseremailcom', self.params['password'])
        self.assertEqual(response.status_code, 400)

    def test_blank_email_can_authenticate(self):
        user, response = self.create_user_and_response('', self.params['password'])
        self.assertEqual(response.status_code, 400)

    def test_no_email_can_authenticate(self):
        user, response = self.create_user_and_response(email=None, password=self.params['password'])
        self.assertEqual(response.status_code, 400)

    def test_incorrect_password_can_authenticate(self):
        password = self.params['password'] + '----'
        user, response = self.create_user_and_response(self.params['email'], password)
        self.assertEqual(response.status_code, 400)

    def test_blank_password_can_authenticate(self):
        user, response = self.create_user_and_response(self.params['email'], '')
        self.assertEqual(response.status_code, 400)

    def test_no_password_can_authenticate(self):
        user, response = self.create_user_and_response(email=self.params['email'], password=None)
        self.assertEqual(response.status_code, 400)

