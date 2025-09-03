from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant

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

    def test_raises_a_validation_error_if_the_unique_id_is_null(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id=None)

    def test_raises_a_validation_error_if_the_unique_id_is_empty(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id="")
