from django.test import TestCase
from datetime import datetime, date
from django.core.exceptions import ValidationError


from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.date_response import DateResponse
from lung_cancer_screening.questions.models.boolean_response import BooleanResponse

class TestParticipant(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")

    def test_has_unique_id_as_a_string(self):
        self.assertIsInstance(
            self.participant.unique_id,
            str
        )

    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.participant.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.participant.updated_at,
            datetime
        )

    def test_has_many_boolean_responses(self):
        boolean_response = BooleanResponse.objects.create(
            value=True,
            participant=self.participant,
            question="Asking something else generic?"
        )
        self.assertIn(boolean_response, list(self.participant.booleanresponse_set.all()))

    def test_has_many_date_responses(self):
        date_response = DateResponse.objects.create(
            value=date(2000, 9, 8),
            participant=self.participant,
            question="Asking something generic?"
        )
        self.assertIn(date_response, list(self.participant.dateresponse_set.all()))

    def test_has_many_responses(self):
        boolean_response = BooleanResponse.objects.create(
            value=True,
            participant=self.participant,
            question="Asking something else generic?"
        )
        date_response = DateResponse.objects.create(
            value=date(2000, 9, 8),
            participant=self.participant,
            question="Asking something generic?"
        )

        responses = self.participant.responses()
        self.assertIn(boolean_response, responses)
        self.assertIn(date_response, responses)

    def test_raises_a_validation_error_if_the_unique_id_is_null(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id=None)

    def test_raises_a_validation_error_if_the_unique_id_is_empty(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id="")
