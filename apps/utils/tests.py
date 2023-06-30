from django.test import TestCase
from .models import Dummy


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
