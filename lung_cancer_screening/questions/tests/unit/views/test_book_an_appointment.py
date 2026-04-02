from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user

@tag("BookAnAppointment")
class TestGetBookAnAppointment(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("questions:book_an_appointment"))

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/call-us-to-book-an-appointment",
            fetch_redirect_response=False,
        )
