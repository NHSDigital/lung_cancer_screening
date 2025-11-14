from django.test import TestCase
from django.urls import reverse

from lung_cancer_screening.questions.models.participant import Participant


class TestRespiratoryConditions(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()
        self.valid_params = {"respiratory_conditions": ["P", "E"]}

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:respiratory_conditions"))
        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:respiratory_conditions"))
        self.assertContains(response, "Have you ever been diagnosed with any of the following respiratory conditions?")
        self.assertContains(response, "Pneumonia")
        self.assertContains(response, "Emphysema")
        self.assertContains(response, "Chronic bronchitis")
        self.assertContains(response, "Tuberculosis (TB)")
        self.assertContains(response, "Chronic obstructive pulmonary disease (COPD)")
        self.assertContains(response, "None of the above")

    def test_post_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_for_the_participant(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(
            response_set.respiratory_conditions,
            self.valid_params["respiratory_conditions"]
        )
        self.assertEqual(response_set.participant, self.participant)

    def test_post_stores_single_selection(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["N"]}
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(
            response_set.respiratory_conditions,
            ["N"]
        )

    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertEqual(response.status_code, 302)

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_responds_with_422_if_no_selection_is_made(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": []}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        self.assertEqual(
            self.participant.responseset_set.first().respiratory_conditions,
            None
        )
