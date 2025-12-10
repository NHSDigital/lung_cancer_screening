from django.test import TestCase
from django.urls import reverse

class TestGetStart(TestCase):

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:start"))

        self.assertEqual(response.status_code, 200)
