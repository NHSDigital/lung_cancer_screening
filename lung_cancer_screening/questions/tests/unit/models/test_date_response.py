from django.test import TestCase
from datetime import datetime, date
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.date_response import DateResponse

class TestDateResponse(TestCase):
    def setUp(self):
        participant = Participant.objects.create(unique_id="12345")
        self.date_response = DateResponse.objects.create(
            value=date(2000, 1, 1),
            participant=participant,
            question="Asking something generic?"
        )

    # def test_beloings_to_participant_as_a_string(self):
    #     self.assertIsInstance(
    #         self.date_response.participant_id,
    #         str
    #     )

    def test_has_value_as_a_date(self):
        self.assertIsInstance(
            self.date_response.value,
            date
        )

    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.date_response.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.date_response.updated_at,
            datetime
        )

    def test_raises_a_validation_error_if_the_value_is_null(self):
        with self.assertRaises(ValidationError):
            DateResponse.objects.create(value=None)

    def test_raises_a_validation_error_if_the_question_is_null(self):
        with self.assertRaises(ValidationError):
            DateResponse.objects.create(question=None)
