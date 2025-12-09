from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user

from lung_cancer_screening.questions.models.participant import Participant

class TestYourResults(TestCase):
    def setUp(self):
        login_user(self.client)

        participant = Participant.objects.create(unique_id="12345")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        participant = Participant.objects.create(unique_id="abcdef")
        self.client.logout()
        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.get(
            reverse("questions:your_results")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/your-results", fetch_redirect_response=False)

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:your_results"))

        self.assertEqual(response.status_code, 200)
