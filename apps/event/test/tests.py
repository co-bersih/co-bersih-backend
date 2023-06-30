from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.user.test.utils import UserManager
from apps.event.models import Event


# Create your tests here.
class CRUDEventTest(TestCase):
    EVENT_LIST_URL = reverse('event-list')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)

        register_data = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_manager.login_user(register_data)
        self.created_event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }

    def create_event(self, created_event_data):
        response = self.client.post(self.EVENT_LIST_URL, created_event_data)
        return response.data['id']

    def test_create_list_event(self):
        total = 10

        for i in range(total):
            self.created_event_data['name'] = f'{self.created_event_data["name"]}{i}'
            self.client.post(self.EVENT_LIST_URL, self.created_event_data)

        response = self.client.get(self.EVENT_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], total)

    def test_create_event(self):
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_without_credentials(self):
        self.user_manager.logout_user()
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event_with_invalid_date(self):
        self.created_event_data['start_date'] = '2023-01-03'
        response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('invalid_date' in response.data.keys())

    def test_retrieve_event(self):
        create_response = self.client.post(self.EVENT_LIST_URL, self.created_event_data)
        created_event_id = create_response.data['id']
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})

        retrieve_response = self.client.get(event_detail_url)
        self.assertEquals(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEquals(retrieve_response.data['id'], created_event_id)
        self.assertTrue('staffs' in retrieve_response.data.keys())
        self.assertTrue('supports' in retrieve_response.data.keys())

    def test_patch_event(self):
        created_event_id = self.create_event(self.created_event_data)
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})

        updated_data = {
            'name': 'event cobersih update'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], updated_data['name'])

    def test_patch_event_invalid_start_date(self):
        created_event_id = self.create_event(self.created_event_data)
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})

        updated_data = {
            'start_date': '2023-01-03'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('invalid_date' in response.data.keys())

    def test_patch_event_invalid_end_date(self):
        created_event_id = self.create_event(self.created_event_data)
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})

        updated_data = {
            'end_date': '2022-01-01'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('invalid_date' in response.data.keys())

    def test_delete_event(self):
        created_event_id = self.create_event(self.created_event_data)
        event_detail_url = reverse('event-detail', kwargs={'pk': created_event_id})
        response = self.client.delete(event_detail_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(len(Event.objects.all()) == 0)

    def test_join_event(self):
        created_event_id = self.create_event(self.created_event_data)

        register_data = self.user_manager.register_user({
            'email': 'user_cobersih2@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih2',
            'bio': 'user2 bio'
        })
        self.user_manager.login_user(register_data)

        join_event_url = reverse('event-join', kwargs={'pk': created_event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_join_event_as_host(self):
        created_event_id = self.create_event(self.created_event_data)
        join_event_url = reverse('event-join', kwargs={'pk': created_event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
