from django.test import TestCase
from .models import Mlcmp


class mlcmpModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Mlcmp.objects.create(result='democrat')

    def test_result(self):
        mlcmp = Mlcmp.objects.get(id=1)
        expected_object_name = f'{mlcmp.result}'
        self.assertEquals(expected_object_name, 'democrat')

