from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import User
import uuid


# Create your tests here.
class RegisterTest(TestCase):
    register_url = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.data)
        self.assertEquals(response.data['email'], self.data['email'])
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_email_exist(self):
        User.objects.create(**self.data)
        response = self.client.post(self.register_url, self.data)
        self.assertIsInstance(response.data['email'][0], ErrorDetail)

    def test_email_invalid(self):
        self.data['email'] = 'invalid_email'
        response = self.client.post(self.register_url, self.data)
        self.assertIsInstance(response.data['email'][0], ErrorDetail)

    def test_password_empty(self):
        self.data['password'] = ''
        response = self.client.post(self.register_url, self.data)
        self.assertIsInstance(response.data['password'][0], ErrorDetail)

    def test_name_empty(self):
        self.data['name'] = ''
        response = self.client.post(self.register_url, self.data)
        self.assertIsInstance(response.data['name'][0], ErrorDetail)


class LoginTest(TestCase):
    login_url = reverse('user-login')
    register_url = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }
        self.client.post(self.register_url, self.data)

    def test_login_user(self):
        login_data = {
            'email': self.data['email'],
            'password': self.data['password'],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_password_invalid(self):
        login_data = {
            'email': self.data['email'],
            'password': 'invalid_password',
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_email_invalid(self):
        login_data = {
            'email': 'invalid_email',
            'password': self.data['password'],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailTest(TestCase):
    register_url = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }
        response = self.client.post(self.register_url, self.data)

        self.user_detail = response.data
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user_detail['id']})

    def test_user_detail(self):
        response = self.client.get(f'{self.user_detail_url}')
        self.assertEquals(response.data, self.user_detail)

    def test_invalid_user_detail(self):
        self.user_detail_url = reverse('user-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(f'{self.user_detail_url}')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class PatchUserDetailTest(TestCase):
    register_url = reverse('user-register')
    login_url = reverse('user-login')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }
        register_response = self.client.post(self.register_url, self.data)
        self.user_detail = register_response.data
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user_detail['id']})

        login_data = {
            'email': self.data['email'],
            'password': self.data['password'],
        }
        login_response = self.client.post(self.login_url, login_data)
        self.token = login_response.data

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])
        updated_data = {
            'password': 'new_password'
        }
        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_change_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])

        updated_data = {
            'name': 'user_cobersih_new_name'
        }

        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user_instance = User.objects.get(id=self.user_detail['id'])
        self.assertEquals(user_instance.name, updated_data['name'])


class CreateUserTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.data)
        self.assertTrue(isinstance(user, User))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.data)
        self.assertTrue(superuser.is_superuser)

    def test_string_representation(self):
        user = User.objects.create_user(**self.data)
        self.assertEquals(str(user), user.name)
