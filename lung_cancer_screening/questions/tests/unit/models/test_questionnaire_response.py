from django.test import TestCase
from datetime import datetime, date

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.questionnaire_response import QuestionnaireResponse

class TestQuestionnaireResponse(TestCase):
    def setUp(self):
        participant = Participant.objects.create(unique_id="12345")
        self.questionnaire_response = QuestionnaireResponse.objects.create(
            value=date(2000, 1, 1),
            participant=participant
        )

    # def test_beloings_to_participant_as_a_string(self):
    #     self.assertIsInstance(
    #         self.questionnaire_response.participant_id,
    #         str
    #     )

    def test_has_value_as_a_date(self):
        self.assertIsInstance(
            self.questionnaire_response.value,
            date
        )

    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.questionnaire_response.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.questionnaire_response.updated_at,
            datetime
        )
