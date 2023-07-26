import json

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.event.models import Event, Payment
from apps.event.test.utils import EventManager
from apps.user.models import User
from apps.user.test.utils import UserManager
from apps.report.test.utils import ReportManager
from apps.report.models import Report


# Create your tests here.
class CRUDEventTest(TestCase):
    EVENT_LIST_URL = reverse('event-list')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.report_manager = ReportManager(self.client)

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
        self.verify_event(self.event_id)

    def create_event(self, event_data):
        response = self.client.post(self.EVENT_LIST_URL, event_data)
        return response.data['id']

    def verify_event(self, event_id):
        event = Event.objects.get(pk=event_id)
        event.is_verified = True
        event.save()

    def test_create_list_verified_event(self):
        initial = len(Event.objects.all())
        total = 10

        for i in range(total):
            self.event_data['name'] = f'{self.event_data["name"]}{i}'
            event_id = self.create_event(self.event_data)
            self.verify_event(event_id)

        response = self.client.get(self.EVENT_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], initial + total)

    def test_create_event_with_report_ref(self):
        report_data = {
            'title': 'report cobersih',
            'description': 'deskripsi report cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
        }

        report_id = self.report_manager.create_report(report_data)

        new_event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'report_ref_id': report_id,
        }

        response = self.client.post(self.EVENT_LIST_URL, new_event_data)
        event_id = response.data['id']

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(pk=event_id).exists())
        self.assertFalse(Report.objects.filter(pk=report_id).exists())

    def test_create_event_with_invalid_report_ref(self):
        new_event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'report_ref_id': '00000000-00000000-00000000-00000000',
        }

        response = self.client.post(self.EVENT_LIST_URL, new_event_data)
        event_id = response.data['id']

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(pk=event_id).exists())

    def test_create_event_with_invalid_uuid_report_ref(self):
        new_event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'report_ref_id': 'a',
        }

        response = self.client.post(self.EVENT_LIST_URL, new_event_data)
        event_id = response.data['id']

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(pk=event_id).exists())

    def test_find_list_verified_event_by_name(self):
        total = 10

        for i in range(total):
            self.event_data['name'] = f'{self.event_data["name"]}{i}'
            event_id = self.create_event(self.event_data)
            self.verify_event(event_id)

        response = self.client.get(f'{self.EVENT_LIST_URL}?search={self.event_data["name"]}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_find_list_unverified_event(self):
        total_unverified_event = 10

        for i in range(total_unverified_event):
            self.event_data['name'] = f'{self.event_data["name"]}{i}'
            event_id = self.create_event(self.event_data)

        response = self.client.get(f'{self.EVENT_LIST_URL}?is_verified=False')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], total_unverified_event)

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

    def test_no_pagination_for_distance_query(self):
        distance_query_url = reverse('event-list')
        response = self.client.get(f'{distance_query_url}?lon=0&lat=0&min=0')
        self.assertIsInstance(response.data[0], dict)


class EventActionTest(TestCase):
    ACCEPT_PAYMENT_URL = reverse('event-accept-payment')

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
        self.event_manager.verify_event(self.event_id)

        self.payment_data = {
            "link_id": 1,
            "link_url": "flip.id/pwf-sandbox/$test/#test",
            "title": "test2",
            "type": "MULTIPLE",
            "amount": 0,
            "redirect_url": "",
            "expired_date": None,
            "created_from": "API",
            "status": "ACTIVE",
            "is_address_required": 0,
            "is_phone_number_required": 0,
            "step": 1
        }

        # Add payment to event
        payment = Payment.objects.create(**self.payment_data)
        event = Event.objects.get(pk=self.event_id)
        event.payment = payment
        event.save()

    def test_join_verified_event(self):
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_join_unverified_event(self):
        self.event_manager.unverify_event(self.event_id)

        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_leave_verified_event(self):
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        self.client.post(join_event_url)

        leave_event_url = reverse('event-leave', kwargs={'pk': self.event_id})
        response = self.client.post(leave_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_leave_unverified_event(self):
        self.event_manager.unverify_event(self.event_id)

        self.user_manager.login_user(self.user2)
        leave_event_url = reverse('event-leave', kwargs={'pk': self.event_id})
        response = self.client.post(leave_event_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_join_event_as_host(self):
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_event_as_staff(self):
        # Update user2 as user1 event staff
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})

        # Login as user2
        self.user_manager.login_user(self.user2)
        join_event_url = reverse('event-join', kwargs={'pk': self.event_id})
        response = self.client.post(join_event_url)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_event_staffs(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(User.objects.get(pk=self.user2['id']).events_staff.all()) == 1)

    def test_update_event_staffs_with_invalid_id(self):
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_email': 'invalid@mail.com'})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'staff_email')

    def test_update_event_staffs_with_invalid_user(self):
        self.user_manager.login_user(self.user2)

        # Update event as another user
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        response = self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data['errors'][0]['code'] == 'permission_denied')

    def test_remove_event_staffs(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})

        # Remove new staff
        delete_staff_event_url = reverse('event-staff-detail',
                                         kwargs={'pk': self.event_id, 'staff_email': self.user2['email']})
        response = self.client.delete(delete_staff_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(User.objects.get(pk=self.user2['id']).events_staff.all()) == 0)

    def test_remove_event_staffs_with_invalid_user(self):
        # Update event with new staff (another_user_detail)
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': self.event_id})
        self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})

        # Login as user2
        self.user_manager.login_user(self.user2)

        # Remove new staff
        delete_staff_event_url = reverse('event-staff-detail',
                                         kwargs={'pk': self.event_id, 'staff_email': self.user2['email']})
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
        response = self.client.post(update_staff_event_url, {'staff_email': self.user2['email']})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        event = Event.objects.get(pk=self.event_id)
        self.assertTrue(len(event.staffs.all()) == 2)  # staffs: user1 (host) and user2
        self.assertTrue(len(event.joined_users.all()) == 0)  # joined_user : None

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

    def test_accept_payment(self):
        payload = {
            "token": settings.FLIP_VALIDATION_TOKEN,
            "data": json.dumps({
                "id": "FT1",
                "bill_link": "flip.id/pwf-sandbox/$test/#test",
                "bill_link_id": self.payment_data['link_id'],
                "bill_title": "Cimol Goreng",
                "sender_name": "Jon Doe",
                "sender_bank": "bni",
                "sender_email": "email@email.com",
                "amount": 10000,
                "status": "SUCCESSFUL",
                "sender_bank_type": "bank_account",
                "created_at": "2021-11-29 10:10:10"
            })
        }

        response = self.client.post(self.ACCEPT_PAYMENT_URL, payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        event = Event.objects.get(pk=self.event_id)
        data = json.loads(payload['data'])
        self.assertEquals(event.total_donation, data['amount'])

    def test_accept_payment_with_invalid_token(self):
        payload = {
            "token": "<invalid_token>",
            "data": json.dumps({
                "id": "FT1",
                "bill_link": "flip.id/pwf-sandbox/$test/#test",
                "bill_link_id": self.payment_data['link_id'],
                "bill_title": "Cimol Goreng",
                "sender_name": "Jon Doe",
                "sender_bank": "bni",
                "sender_email": "email@email.com",
                "amount": 10000,
                "status": "SUCCESSFUL",
                "sender_bank_type": "bank_account",
                "created_at": "2021-11-29 10:10:10"
            })
        }

        response = self.client.post(self.ACCEPT_PAYMENT_URL, payload)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_payment_with_FAILED_status(self):
        payload = {
            "token": settings.FLIP_VALIDATION_TOKEN,
            "data": json.dumps({
                "id": "FT1",
                "bill_link": "flip.id/pwf-sandbox/$test/#test",
                "bill_link_id": self.payment_data['link_id'],
                "bill_title": "Cimol Goreng",
                "sender_name": "Jon Doe",
                "sender_bank": "bni",
                "sender_email": "email@email.com",
                "amount": 10000,
                "status": "FAILED",
                "sender_bank_type": "bank_account",
                "created_at": "2021-11-29 10:10:10"
            })
        }

        response = self.client.post(self.ACCEPT_PAYMENT_URL, payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        event = Event.objects.get(pk=self.event_id)
        data = json.loads(payload['data'])
        self.assertNotEquals(event.total_donation, data['amount'])


class EventJoinedUserTest(TestCase):
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
        self.user3 = self.user_manager.register_user({
            'email': 'user_cobersih3@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih3',
            'bio': 'user2 bio'
        })
        self.event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }

        # Create event as user1
        self.user_manager.login_user(self.user1)
        self.event_id = self.event_manager.create_event(self.event_data)
        self.event_manager.verify_event(self.event_id)

        # Add user2 as staff
        self.event_manager.add_staff(self.event_id, self.user2['email'])

        # user3 joined event
        self.user_manager.login_user(self.user3)
        self.event_manager.join_event(self.event_id)

    def test_get_joined_user_as_host(self):
        self.user_manager.login_user(self.user1)

        event_joined_user_url = reverse('event-joined-user-list', kwargs={'pk': self.event_id})
        response = self.client.get(event_joined_user_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_get_joined_user_as_staff(self):
        self.user_manager.login_user(self.user2)

        event_joined_user_url = reverse('event-joined-user-list', kwargs={'pk': self.event_id})
        response = self.client.get(event_joined_user_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_get_joined_user_as_joined_user(self):
        self.user_manager.login_user(self.user3)

        event_joined_user_url = reverse('event-joined-user-list', kwargs={'pk': self.event_id})
        response = self.client.get(event_joined_user_url)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_joined_user_as_anon(self):
        self.user_manager.logout_user()

        event_joined_user_url = reverse('event-joined-user-list', kwargs={'pk': self.event_id})
        response = self.client.get(event_joined_user_url)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventFilterTest(TestCase):
    EVENT_LIST_URL = reverse('event-list')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.event_manager = EventManager(self.client)

        self.user = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })

        self.event_data1 = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-10'
        }

        self.event_data2 = {
            'name': 'event cobersih2',
            'description': 'deskripsi event cobersih2',
            'preparation': 'persiapan event cobersih2',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-11',
            'end_date': '2023-01-20'
        }

        # Create event1 (verified) and event2 (unverified)
        self.user_manager.login_user(self.user)
        self.event1_id = self.event_manager.create_event(self.event_data1)
        self.event_manager.verify_event(self.event1_id)
        self.event2_id = self.event_manager.create_event(self.event_data2)

    def test_event_filter_by_start_date(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?start_date=2023-01-01')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_event_filter_by_start_date_lt(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?start_date__lt=2023-01-01')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 0)

    def test_event_filter_by_start_date_lte(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?start_date__lte=2023-01-01')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_event_filter_by_end_date(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?end_date=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_event_filter_by_end_date_gt(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?end_date__gt=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_end_date_gt_and_verified(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?is_verified=true&end_date__gt=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 0)

    def test_end_date_gte_and_verified(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?is_verified=true&end_date__gte=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_end_date_gt_and_unverified(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?is_verified=false&end_date__gt=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_end_date_gte_and_unverified(self):
        response = self.client.get(f'{self.EVENT_LIST_URL}?is_verified=false&end_date__gte=2023-01-10')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)
