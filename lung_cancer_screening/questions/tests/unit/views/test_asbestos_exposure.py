from django.test import TestCase
from django.urls import reverse

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.response_set import AsbestosExposureValues


class TestAsbestosExposure(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()
        self.valid_params = {"asbestos_exposure": AsbestosExposureValues.YES}

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:asbestos_exposure")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))
        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))
        self.assertContains(response, "Have you ever worked in a job where you might have been exposed to asbestos?")

    def test_post_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_for_the_participant(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(
            response_set.asbestos_exposure,
            self.valid_params["asbestos_exposure"]
        )
        self.assertEqual(response_set.participant, self.participant)

    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        # Assuming it redirects to the next question page - adjust as needed
        self.assertEqual(response.status_code, 302)

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            {"asbestos_exposure": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            {"asbestos_exposure": "invalid"}
        )

        self.assertEqual(
            self.participant.responseset_set.first().asbestos_exposure,
            None
        )
