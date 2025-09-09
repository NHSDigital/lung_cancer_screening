from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from lung_cancer_screening.questions.models.participant import Participant

class TestStart(TestCase):

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:start"))

        self.assertEqual(response.status_code, 200)

    def test_post_creates_a_new_participant_and_response_set(self):
        self.client.post(
            reverse("questions:start"),
            {"participant_id": "12345"}
        )

        participant = Participant.objects.all().last()
        self.assertEqual(participant.unique_id, "12345")
        self.assertEqual(participant.responseset_set.count(), 1)

    def test_post_creates_a_new_response_set_if_the_participant_already_exists_and_has_no_response_set_submitted_in_the_last_year(self):
        participant = Participant.objects.create(unique_id="12345")
        old_response_set = participant.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=365)
        )

        self.client.post(
            reverse("questions:start"),
            {"participant_id": participant.unique_id}
        )

        self.assertEqual(participant.responseset_set.count(), 2)
        self.assertNotEqual(participant.responseset_set.last().id, old_response_set.id)

    def test_post_shows_an_error_if_a_response_set_was_submitted_within_the_last_year(self):
        participant = Participant.objects.create(unique_id="12345")
        participant.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:start"),
            {"participant_id": participant.unique_id}
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn(
            "Responses have already been submitted for this participant",
            response.text
        )

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

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_post_responds_with_422_if_the_participant_fails_to_create(self):
        response = self.client.post(
            reverse("questions:start"),
            {"participant_id": ""}
        )

        self.assertEqual(response.status_code, 422)

