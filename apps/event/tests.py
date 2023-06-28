from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail


# Create your tests here.
class CRUDEventTest(TestCase):
    REGISTER_URL = reverse('user-register')
    LOGIN_URL = reverse('user-login')
    EVENT_LIST_URL = reverse('event-list')

    def setUp(self):
        self.client = APIClient()
        register_data = self.register_user()
        self.login_user(register_data)
        self.created_event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }

    def login_user(self, register_data):
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response = self.client.post(self.LOGIN_URL, login_data)
        self.token = response.data

    def register_user(self):
        register_data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'password',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }
        self.client.post(self.REGISTER_URL, register_data)
        return register_data

    def test_create_list_event(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])
        total = 10

        for i in range(total):
            self.created_event_data['name'] = f'{self.created_event_data["name"]}{i}'
            self.client.post(self.EVENT_LIST_URL, self.created_event_data)

        response = self.client.get(self.EVENT_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], total)

    def test_create_event(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_without_credentials(self):
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event_with_invalid_date(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])
        self.created_event_data['start_date'] = '2023-01-03'
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data['non_field_errors'][0], ErrorDetail)

    def test_retrieve_event(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token['access'])
        create_response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)

        created_event_id = create_response.data['id']
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})

        retrieve_response = self.client.get(event_detail_url)
        self.assertEquals(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEquals(retrieve_response.data['id'], created_event_id)
        self.assertTrue('staffs' in retrieve_response.data.keys())
        self.assertTrue('supports' in retrieve_response.data.keys())
