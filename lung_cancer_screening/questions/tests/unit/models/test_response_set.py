from django.test import TestCase
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django.core.exceptions import ValidationError

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

    def test_has_height_as_a_int(self):
        self.response_set.height = 1700
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.height,
            int
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

    def test_has_submitted_at_as_null_by_default(self):
        self.assertIsNone(
            self.response_set.submitted_at
        )

    def test_has_submitted_at_as_a_datetime(self):
        self.response_set.submitted_at = datetime.now()

        self.assertIsInstance(
            self.response_set.submitted_at,
            datetime
        )

    def test_is_invalid_if_another_unsubmitted_response_set_exists(self):
        participant = Participant.objects.create(unique_id="56789")
        participant.responseset_set.create(submitted_at=None)

        with self.assertRaises(ValidationError) as context:
            participant.responseset_set.create(submitted_at=None)

        self.assertEqual(
            context.exception.messages[0],
            "An unsubmitted response set already exists for this participant"
        )

    def test_is_invalid_if_another_response_set_was_submitted_within_the_last_year(self):
        participant = Participant.objects.create(unique_id="56789")
        participant.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        with self.assertRaises(ValidationError) as context:
            participant.responseset_set.create()

        self.assertEqual(
            context.exception.messages[0],
            "Responses have already been submitted for this participant"
        )

    def test_is_invalid_if_height_is_below_lower_bound(self):
        self.response_set.height = 1396

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages
        )

    def test_is_invalid_if_height_is_above_upper_bound(self):
        self.response_set.height = 2439

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages
        )
