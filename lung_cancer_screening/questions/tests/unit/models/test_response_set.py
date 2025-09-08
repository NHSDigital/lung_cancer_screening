from django.test import TestCase
from datetime import datetime, date

from ....models.participant import Participant
from ....models.response_set import HaveYouEverSmokedValues

class TestResponseSet(TestCase):
    def setUp(self):
        participant = Participant.objects.create(unique_id="12345")
        self.response_set = participant.responseset_set.create()

    def test_has_have_you_ever_smoked_as_an_enum(self):
        self.response_set.have_you_ever_smoked = HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        self.response_set.save()

        self.assertEqual(
            self.response_set.get_have_you_ever_smoked_display(),
            HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.label
        )

    def test_has_date_of_birth_as_a_date(self):
        self.response_set.date_of_birth = date(2000, 9, 8)
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.date_of_birth,
            date
        )

    def test_has_a_participant_as_a_foreign_key(self):
        self.assertIsInstance(
            self.response_set.participant,
            Participant
        )

    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.response_set.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.response_set.updated_at,
            datetime
        )
