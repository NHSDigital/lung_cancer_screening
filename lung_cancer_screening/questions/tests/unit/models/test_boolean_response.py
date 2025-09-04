from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.boolean_response import BooleanResponse

class TestBooleanResponse(TestCase):
    def setUp(self):
        participant = Participant.objects.create(unique_id="12345")
        self.boolean_response = BooleanResponse.objects.create(
            value=True,
            participant=participant,
            question="Asking something generic?"
        )

    # def test_beloings_to_participant_as_a_string(self):
    #     self.assertIsInstance(
    #         self.boolean_response.participant_id,
    #         str
    #     )

    def test_has_value_as_a_boolean(self):
        self.assertIsInstance(
            self.boolean_response.value,
            bool
        )

    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.boolean_response.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.boolean_response.updated_at,
            datetime
        )

    def test_raises_a_validation_error_if_the_value_is_null(self):
        with self.assertRaises(ValidationError):
            BooleanResponse.objects.create(value=None)

    def test_raises_a_validation_error_if_the_question_is_null(self):
        with self.assertRaises(ValidationError):
            BooleanResponse.objects.create(question=None)
