from django.test import TestCase
from .models import Dummy, GeoLocation
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.
class DummyTest(TestCase):
    def test_delete_model(self):
        dummy = Dummy(name='dummy')
        dummy.save()
        dummy.delete()

        self.assertTrue(dummy.is_deleted)

    def test_get_all_dummy(self):
        dummy1 = Dummy.objects.create(name='dummy1')
        dummy2 = Dummy.objects.create(name='dummy2')
        dummy1.delete()

        all_dummies = Dummy.objects.all()
        self.assertTrue(len(all_dummies) == 1)
        self.assertTrue(dummy1 not in all_dummies)
        self.assertTrue(dummy2 in all_dummies)

    def test_filter_dummy(self):
        dummy1 = Dummy.objects.create(name='dummy1')
        dummy2 = Dummy.objects.create(name='dummy2')
        dummy1.delete()

        filtered_dummies = Dummy.objects.filter(name__contains='dummy')
        self.assertTrue(len(filtered_dummies) == 1)
        self.assertTrue(dummy1 not in filtered_dummies)
        self.assertTrue(dummy2 in filtered_dummies)


class GeoLocationTest(TestCase):
    LOCATION_LIST_URL = reverse('location-list')

    def setUp(self):
        self.client = APIClient()
        self.target_latitude = -6.121223675912693
        self.target_longitude = 106.82894663122536
        GeoLocation.objects.create(name='Ciliwung', latitude=-6.121223675912693, longitude=106.82894663122536)
        GeoLocation.objects.create(name='Dunia Fantasi', latitude=-6.1251535370496555, longitude=106.83356500486798)
        GeoLocation.objects.create(name='Monas', latitude=-6.172070288866705, longitude=106.8279923720938)
        GeoLocation.objects.create(name='Kota Tua', latitude=-6.1375305331867915, longitude=106.81838522592501)

    def test_get_location_0_km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&max=0'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_get_location_2_km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&max=2'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 2)

    def test_get_location_4_km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&max=4'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 3)

    def test_get_location_6_km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&max=10'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 4)

    def test_get_location_2km_to_4km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=2&max=4'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_get_location_min_2km_from_target(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=2'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 2)

    def test_get_location_invalid_param(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=a&max=10'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=10&max=b'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_location_negative_param(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=-10&max=100'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=10&max=-100'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_location_max_lt_min(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}&min=100&max=10'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_location_without_min_and_max(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}&lon={self.target_longitude}'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 4)

    def test_get_location_without_lat(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lon={self.target_longitude}'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 4)

    def test_get_location_without_lon(self):
        response = self.client.get(
            f'{self.LOCATION_LIST_URL}?lat={self.target_latitude}'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 4)

    def test_get_location_without_param(self):
        response = self.client.get(self.LOCATION_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 4)
