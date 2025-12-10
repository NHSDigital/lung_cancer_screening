from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone
# from dateutil.relativedelta import relativedelta

# from ...factories.user_factory import UserFactory
from .helpers.authentication import login_user

class TestGetStart(TestCase):

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:start"))

        self.assertEqual(response.status_code, 200)
