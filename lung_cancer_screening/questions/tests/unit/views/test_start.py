from django.test import TestCase
from django.urls import reverse
from datetime import date

from lung_cancer_screening.questions.models.participant import Participant

class TestStart(TestCase):

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:start"))

        self.assertEqual(response.status_code, 200)

    def test_post_creates_a_new_participant(self):
        self.client.post(
            reverse("questions:start"),
            {"participant_id": "12345"}
        )

        self.assertEqual(Participant.objects.all().last().unique_id, "12345")

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:start"),
            {"participant_id": "12345"}
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_the_date_of_birth_path(self):
        response = self.client.post(
            reverse("questions:start"),
            {"participant_id": "12345"}
        )

        self.assertRedirects(response, reverse("questions:date_of_birth"))

    def test_post_responds_with_422_if_the_participant_fails_to_create(self):
        response = self.client.post(
            reverse("questions:start"),
            {"participant_id": ""}
        )

        self.assertEqual(response.status_code, 422)
