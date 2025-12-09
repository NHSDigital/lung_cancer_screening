from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user

from lung_cancer_screening.questions.models.participant import Participant

class TestPostAgeRangeExit(TestCase):
    def setUp(self):
        login_user(self.client)

        participant = Participant.objects.create(unique_id="12345")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        participant = Participant.objects.create(unique_id="abcdef")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/age-range-exit", fetch_redirect_response=False)

    def test_get_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:age_range_exit"))

        self.assertEqual(response.status_code, 200)
