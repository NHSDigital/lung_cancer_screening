from django.test import TestCase
from django.urls import reverse

class TestRoot(TestCase):

    def test_redirects_to_start(self):
        response = self.client.get(reverse("questions:root"))

        self.assertRedirects(response, reverse("questions:start"))
