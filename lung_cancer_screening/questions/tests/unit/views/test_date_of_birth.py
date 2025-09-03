from django.test import TestCase
from django.urls import reverse
from datetime import date

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.questionnaire_response import QuestionnaireResponse

class TestPostDateOfBirth(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_participant_id_in_the_form(self):
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertContains(
            response,
            f"<input type=\"hidden\" name=\"participant_id\" value=\"{self.participant.unique_id}\">"
        )

    def test_post_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:date_of_birth"),
            {"day": "8", "month": "9", "year": "2000"}
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_questionnaire_response_for_the_participant(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            {"day": "8", "month": "9", "year": "2000"}
        )

        questionnaire_response = QuestionnaireResponse.objects.first()
        self.assertEqual(questionnaire_response.value, date(2000, 9, 8))
        self.assertEqual(questionnaire_response.participant, self.participant)

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            {"day": "8", "month": "9", "year": "2000"}
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_responses_path(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {"day": "8", "month": "9", "year": "2000"}
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_questionnaire_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {"day": "80000", "month": "90000", "year": "20000000"}
        )

        self.assertEqual(response.status_code, 422)
