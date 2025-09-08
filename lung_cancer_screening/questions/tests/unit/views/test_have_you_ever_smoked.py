from django.test import TestCase
from django.urls import reverse

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.boolean_response import BooleanResponse

class TestHaveYouEverSmoked(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.valid_params = { "value": True }

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:have_you_ever_smoked")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:have_you_ever_smoked"))

        self.assertEqual(response.status_code, 200)

    def test_post_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_boolean_response_for_the_participant(self):
        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        boolean_response = BooleanResponse.objects.first()
        self.assertEqual(boolean_response.value, self.valid_params["value"])
        self.assertEqual(boolean_response.participant, self.participant)
        self.assertEqual(boolean_response.question, "Have you ever smoked?")

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_the_date_of_birth_path(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:date_of_birth"))

    def test_post_responds_with_422_if_the_date_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            {"value": "something not a boolean"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_create_a_date_response_if_the_user_is_not_a_smoker(self):
        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            { "value": False }
        )

        self.assertEqual(BooleanResponse.objects.count(), 0)

    def test_post_redirects_if_the_user_not_a_smoker(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            {"value": False }
        )

        self.assertRedirects(response, reverse("questions:non_smoker_exit"))
