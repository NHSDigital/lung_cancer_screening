from django.test import TestCase
from django.urls import reverse
from datetime import date

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.questionnaire_response import QuestionnaireResponse

class TestResponses(TestCase):

    def setUp(self):
        self.participant = Participant.objects.create(unique_id='12345')

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:start"))

    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:responses"))

        self.assertEqual(response.status_code, 200)

    def test_contains_the_participants_questionnaire_response(self):
        questionnaire_response = QuestionnaireResponse.objects.create(
            value=date(2000, 9, 8),
            participant=self.participant
        )

        response = self.client.get(reverse("questions:responses"))

        self.assertContains(response, questionnaire_response.value)

    def test_does_not_contain_responses_for_other_participants(self):
        other_participant = Participant.objects.create(unique_id='67890')
        other_questionnaire_response = QuestionnaireResponse.objects.create(value=date(1990, 1, 1), participant=other_participant)

        response = self.client.get(reverse("questions:responses"))

        self.assertNotContains(response, other_questionnaire_response.value)
