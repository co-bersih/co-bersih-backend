from apps.event.models import Event
from apps.event.test.utils import EventManager
from apps.user.models import User
from apps.user.test.utils import UserManager

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.
class CRUDEventTest(TestCase):
    EVENT_LIST_URL = reverse('event-list')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)

        self.user1 = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user2 = self.user_manager.register_user({
            'email': 'user_cobersih2@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih2',
            'bio': 'user2 bio'
        })

        # Login as user_1 and create event
        self.user_manager.login_user(self.user1)
        self.event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }
        self.event_id = self.create_event(self.event_data)

    def create_event(self, event_data):
        response = self.client.post(self.EVENT_LIST_URL, event_data)
        return response.data['id']

    def test_create_list_event(self):
        initial = len(Event.objects.all())
        total = 10

        for i in range(total):
            self.event_data['name'] = f'{self.event_data["name"]}{i}'
            self.client.post(self.EVENT_LIST_URL, self.event_data)

        response = self.client.get(self.EVENT_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], initial + total)

    def test_find_list_event_by_name(self):
        total = 10

        for i in range(total):
            self.event_data['name'] = f'{self.event_data["name"]}{i}'
            self.client.post(self.EVENT_LIST_URL, self.event_data)

        response = self.client.get(f'{self.EVENT_LIST_URL}?search={self.event_data["name"]}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_create_event(self):
        response = self.client.post(self.EVENT_LIST_URL, self.event_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(not response.data['is_verified'])

    def test_create_event_without_credentials(self):
        self.user_manager.logout_user()
        response = self.client.post(self.EVENT_LIST_URL, self.event_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event_with_invalid_date(self):
        self.event_data['start_date'] = '2023-01-03'
        response = self.client.post(self.EVENT_LIST_URL, self.event_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['code'] == 'invalid_date')

    def test_retrieve_event(self):
        create_response = self.client.post(self.EVENT_LIST_URL, self.event_data)
        self.created_event_id = create_response.data['id']
        event_detail_url = reverse('event-detail', kwargs={'pk': self.created_event_id})

        retrieve_response = self.client.get(event_detail_url)
        self.assertEquals(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEquals(retrieve_response.data['id'], self.created_event_id)
        self.assertTrue('staffs' in retrieve_response.data.keys())
        self.assertTrue('supports' in retrieve_response.data.keys())

    def test_patch_event(self):
        event_detail_url = reverse('event-detail', kwargs={'pk': self.event_id})

        updated_data = {
            'name': 'event cobersih update'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], updated_data['name'])

    def test_patch_event_invalid_start_date(self):
        event_detail_url = reverse('event-detail', kwargs={'pk': self.event_id})

        updated_data = {
            'start_date': '2023-01-03'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['code'] == 'invalid_date')

    def test_patch_event_invalid_end_date(self):
        event_detail_url = reverse('event-detail', kwargs={'pk': self.event_id})

        updated_data = {
            'end_date': '2022-01-01'
        }

        response = self.client.patch(event_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['code'] == 'invalid_date')

    def test_delete_event(self):
        event_detail_url = reverse('event-detail', kwargs={'pk': self.event_id})
        response = self.client.delete(event_detail_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(len(Event.objects.all()) == 0)


class EventActionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.event_manager = EventManager(self.client)

        self.user1 = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user2 = self.user_manager.register_user({
            'email': 'user_cobersih2@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih2',
            'bio': 'user2 bio'
        })

        # Login as user_1 and create event
        self.user_manager.login_user(self.user1)
        self.event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }
        self.event_id = self.event_manager.create_event(self.event_data)

    def test_join_event(self):
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_leave_event(self):
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        self.client.post(join_event_url)

        leave_event_url = reverse('event-leave', kwargs={'pk': self.event_id})
        response = self.client.post(leave_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_join_event_as_host(self):
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_event_as_staff(self):
        # Update user2 as user1 event staff
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})

        # Login as user2
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_event_staffs(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(User.objects.get(pk=self.user2['id']).events_staff.all()) == 1)

    def test_update_event_staffs_with_invalid_user(self):
        self.user_manager.login_user(self.user2)

        # Update event as another user
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data['errors'][0]['code'] == 'permission_denied')

    def test_remove_event_staffs(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})

        # Remove new staff
        delete_staff_event_url = reverse('event-staff-detail',
                                         kwargs={'pk': self.event_id, 'staff_pk': self.user2['id']})
        response = self.client.delete(delete_staff_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(User.objects.get(pk=self.user2['id']).events_staff.all()) == 0)

    def test_remove_event_staffs_with_invalid_user(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})

        # Login as user2
        self.user_manager.login_user(self.user2)

        # Remove new staff
        delete_staff_event_url = reverse('event-staff-detail',
                                         kwargs={'pk': self.event_id, 'staff_pk': self.user2['id']})
        response = self.client.delete(delete_staff_event_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data['errors'][0]['code'] == 'permission_denied')

    def test_update_event_staffs_as_joined_user(self):
        # Join event as another user
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        self.client.post(join_event_url)

        # Login as host
        self.user_manager.login_user(self.user1)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_id': self.user2['id']})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_event_as_admin(self):
        admin_detail = self.user_manager.create_admin()
        verify_url = reverse('event-verify', kwargs={'pk': self.event_id})

        self.user_manager.login_user(admin_detail)
        response = self.client.post(verify_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_verified'])

    def test_verify_event_as_non_admin(self):
        verify_url = reverse('event-verify', kwargs={'pk': self.event_id})

        response = self.client.post(verify_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_verify_event_as_anon(self):
        self.user_manager.logout_user()
        verify_url = reverse('event-verify', kwargs={'pk': self.event_id})

        response = self.client.post(verify_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
