from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.report.models import Report
from apps.user.test.utils import UserManager


# Create your tests here.
class CRUDReportTest(TestCase):
    REPORT_URL = reverse('report-list')
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

        self.report_data = {
            'title': 'report cobersih',
            'description': 'deskripsi report cobersih',
            'latitude': -6.121133006890128,
            'longitude': 106.82900027912028,
        }

    def create_report(self, report_data):
        report_url = reverse('report-list')
        response = self.client.post(report_url, report_data)
        report_id = response.data['id']
        return report_id

    def test_create_list_report(self):
        self.user_manager.login_user(self.user1)
        total_report = 10

        for i in range(total_report):
            self.create_report(self.report_data)

        response = self.client.get(self.REPORT_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == total_report)

    def test_create_report(self):
        self.user_manager.login_user(self.user1)
        response = self.client.post(self.REPORT_URL, self.report_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.report_data.items() <= response.data.items())

    def test_create_report_with_anon_user(self):
        response = self.client.post(self.REPORT_URL, self.report_data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_report(self):
        self.user_manager.login_user(self.user1)
        create_response = self.client.post(self.REPORT_URL, self.report_data)
        report_id = create_response.data['id']

        report_detail_url = reverse('report-detail', kwargs={'pk': report_id})
        retrieve_response = self.client.get(report_detail_url)
        self.assertEquals(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.report_data.items() <= retrieve_response.data.items())

    def test_delete_report(self):
        self.user_manager.login_user(self.user1)
        create_response = self.client.post(self.REPORT_URL, self.report_data)
        report_id = create_response.data['id']

        report_detail_url = reverse('report-detail', kwargs={'pk': report_id})
        delete_response = self.client.delete(report_detail_url)
        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(len(Report.objects.all()) == 0)

    def test_delete_report_with_invalid_user(self):
        # Create event with user 1
        self.user_manager.login_user(self.user1)
        create_response = self.client.post(self.REPORT_URL, self.report_data)
        report_id = create_response.data['id']

        # Delete event with user 2
        self.user_manager.login_user(self.user2)
        report_detail_url = reverse('report-detail', kwargs={'pk': report_id})
        delete_response = self.client.delete(report_detail_url)
        self.assertEquals(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_report(self):
        self.user_manager.login_user(self.user1)
        create_response = self.client.post(self.REPORT_URL, self.report_data)
        report_id = create_response.data['id']
        report_detail_url = reverse('report-detail', kwargs={'pk': report_id})

        updated_data = {
            'title': 'report cobersih new'
        }

        response = self.client.patch(report_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], updated_data['title'])

    def test_patch_report_with_invalid_user(self):
        self.user_manager.login_user(self.user1)
        create_response = self.client.post(self.REPORT_URL, self.report_data)
        report_id = create_response.data['id']
        report_detail_url = reverse('report-detail', kwargs={'pk': report_id})

        updated_data = {
            'title': 'report cobersih new'
        }

        self.user_manager.login_user(self.user2)
        response = self.client.patch(report_detail_url, updated_data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
