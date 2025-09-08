from django.test import TestCase
from datetime import datetime, date
from django.core.exceptions import ValidationError


from ....models.participant import Participant

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

    def test_has_many_response_sets(self):
        response_set = self.participant.responseset_set.create(
            have_you_ever_smoked=0,
            date_of_birth=date(2000, 9, 8)
        )
        self.assertIn(response_set, list(self.participant.responseset_set.all()))

    def test_raises_a_validation_error_if_the_unique_id_is_null(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id=None)

    def test_raises_a_validation_error_if_the_unique_id_is_empty(self):
        with self.assertRaises(ValidationError):
            Participant.objects.create(unique_id="")
