import uuid
from apps.report.test.utils import ReportManager
from apps.event.test.utils import EventManager
from apps.user.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .utils import UserManager


# Create your tests here.

class RegisterTest(TestCase):
    REGISTER_URL = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }

    def test_register_user(self):
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['email'], self.data['email'])

    def test_email_exist(self):
        User.objects.create(**self.data)
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'email')

    def test_email_invalid(self):
        self.data['email'] = 'invalid_email'
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'email')

    def test_password_empty(self):
        self.data['password'] = ''
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'password')

    def test_password_common(self):
        self.data['password'] = 'password'
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'password')

    def test_name_empty(self):
        self.data['name'] = ''
        response = self.client.post(self.REGISTER_URL, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'name')


class LoginTest(TestCase):
    LOGIN_URL = reverse('user-login')
    REGISTER_URL = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        }
        self.client.post(self.REGISTER_URL, self.data)

    def test_login_user(self):
        login_data = {
            'email': self.data['email'],
            'password': self.data['password'],
        }
        response = self.client.post(self.LOGIN_URL, login_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_password_invalid(self):
        login_data = {
            'email': self.data['email'],
            'password': 'invalid_password',
        }
        response = self.client.post(self.LOGIN_URL, login_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['errors'][0]['code'] == 'no_active_account')

    def test_email_invalid(self):
        login_data = {
            'email': 'invalid_email',
            'password': self.data['password'],
        }
        response = self.client.post(self.LOGIN_URL, login_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['errors'][0]['code'] == 'no_active_account')


class CurrentUserDetailTest(TestCase):
    CURRENT_USER_DETAIL_URL = reverse('current-user-detail')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)

        self.user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })

        self.user_manager.login_user(self.user_detail)

    def test_current_user_detail(self):
        response = self.client.get(self.CURRENT_USER_DETAIL_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['id'], self.user_detail['id'])

    def test_current_user_detail_without_credentials(self):
        self.user_manager.logout_user()
        response = self.client.get(self.CURRENT_USER_DETAIL_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['errors'][0]['code'] == 'not_authenticated')

    def test_current_user_non_admin(self):
        response = self.client.get(self.CURRENT_USER_DETAIL_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_admin'])

    def test_current_user_admin(self):
        admin_data = {
            'email': 'admin@mail.com',
            'password': 'admin',
            'name': 'admin',
            'bio': 'admin bio'
        }
        User.objects.create_superuser(**admin_data)

        self.user_manager.login_user({
            'email': admin_data['email'],
            'password': admin_data['password'],
        })

        response = self.client.get(self.CURRENT_USER_DETAIL_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_admin'])


class UserDetailTest(TestCase):
    REGISTER_URL = reverse('user-register')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user_detail['id']})

    def test_user_detail(self):
        response = self.client.get(f'{self.user_detail_url}')
        self.assertEquals(response.data['id'], self.user_detail['id'])

    def test_invalid_user_detail(self):
        self.user_detail_url = reverse('user-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(f'{self.user_detail_url}')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class PatchUserDetailTest(TestCase):
    REGISTER_URL = reverse('user-register')
    LOGIN_URL = reverse('user-login')

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)

        self.user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user_detail['id']})

        self.user_manager.login_user(self.user_detail)

    def test_change_password(self):
        updated_data = {
            'old_password': self.user_detail['password'],
            'new_password': 'newsecretpass'
        }
        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_change_password_old_password_wrong(self):
        updated_data = {
            'old_password': self.user_detail['password'] + "wrong",
            'new_password': 'newsecretpass'
        }
        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'old_password')

    def test_change_password_new_password_common(self):
        updated_data = {
            'old_password': self.user_detail['password'],
            'new_password': 'password'
        }
        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'new_password')

    def test_change_password_invalid(self):
        """
        User is not allowed to change password without providing `old_password` and `new_password`
        """
        updated_data = {
            'password': 'new_password'
        }
        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_another_user(self):
        # TODO: fix
        another_user_data = {
            'email': 'user2_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user2_cobersih',
            'bio': 'user2 bio'
        }
        another_user_detail = self.user_manager.register_user(another_user_data)
        another_user_detail_url = reverse('user-detail', kwargs={'pk': another_user_detail['id']})

        updated_data = {
            'old_password': 'secretpass',
            'new_password': 'secretpassnew'
        }
        response = self.client.patch(another_user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data['errors'][0]['code'] == 'permission_denied')

    def test_change_name(self):
        updated_data = {
            'name': 'user_cobersih_new_name'
        }

        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user_instance = User.objects.get(id=self.user_detail['id'])
        self.assertEquals(user_instance.name, updated_data['name'])

    def test_change_email(self):
        updated_data = {
            'email': 'user_cobersih_new_email@gmail.com'
        }

        response = self.client.patch(self.user_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['errors'][0]['attr'] == 'email')


class CreateUserTest(TestCase):
    def setUp(self):
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


class UserEventTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.event_manager = EventManager(self.client)

        user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_manager.login_user(user_detail)

        event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }
        self.total_event = 11

        event_ids = self.event_manager.create_events(self.total_event, event_data)

        self.user_manager.logout_user()

        self.another_user_detail = self.user_manager.register_user({
            'email': 'user_cobersih1@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih1',
            'bio': 'user1 bio'
        })
        self.user_manager.login_user(self.another_user_detail)
        self.event_manager.verify_events(event_ids)
        self.event_manager.join_events(event_ids)

    def test_get_user_joined_events(self):
        user_events_url = reverse('user-event-list', kwargs={'pk': self.another_user_detail['id']})
        response = self.client.get(user_events_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == self.total_event)


class UserEventDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.event_manager = EventManager(self.client)

        # Register user1 and user2
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

        # Events data
        self.event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }

        # Create event with user1 as host
        self.user_manager.login_user(self.user1)
        self.event1_id = self.event_manager.create_event(self.event_data)
        self.event_manager.verify_event(self.event1_id)

    def test_check_user_joined_event_is_true(self):
        self.user_manager.login_user(self.user2)
        self.event_manager.join_event(self.event1_id)

        check_event_url = reverse('user-event-detail', kwargs={'pk': self.user2['id'], 'event_pk': self.event1_id})
        response = self.client.head(check_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_check_user_joined_event_is_false(self):
        self.user_manager.login_user(self.user2)

        check_event_url = reverse('user-event-detail', kwargs={'pk': self.user2['id'], 'event_pk': self.event1_id})
        response = self.client.head(check_event_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_joined_event(self):
        self.user_manager.login_user(self.user2)
        self.event_manager.join_event(self.event1_id)

        check_event_url = reverse('user-event-detail', kwargs={'pk': self.user2['id'], 'event_pk': self.event1_id})
        response = self.client.get(check_event_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['id'], self.event1_id)


class UserEventStaffTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.event_manager = EventManager(self.client)

        self.user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_manager.login_user(self.user_detail)

        event_data = {
            'name': 'event cobersih',
            'description': 'deskripsi event cobersih',
            'preparation': 'persiapan event cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }
        self.total_event = 11
        self.event_manager.create_events(self.total_event, event_data)

    def test_get_event_with_user_as_staff(self):
        user_events_staff_url = reverse('user-event-staff-list', kwargs={'pk': self.user_detail['id']})
        response = self.client.get(user_events_staff_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 11)


class UserReportTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager(self.client)
        self.report_manager = ReportManager(self.client)

        self.user_detail = self.user_manager.register_user({
            'email': 'user_cobersih@gmail.com',
            'password': 'secretpass',
            'name': 'user_cobersih',
            'bio': 'user bio'
        })
        self.user_manager.login_user(self.user_detail)

    def test_get_user_reports(self):
        # Create report
        self.report_manager.create_report({
            'title': 'report cobersih',
            'description': 'deskripsi report cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
        })

        user_report_list_url = reverse('user-report-list', kwargs={'pk': self.user_detail['id']})
        response = self.client.get(user_report_list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)
