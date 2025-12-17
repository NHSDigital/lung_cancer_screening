from datetime import datetime, date
from django.test import TestCase
from django.core.exceptions import ValidationError

from ...factories.user_factory import UserFactory


class TestUser(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_has_nhs_number_as_a_string(self):
        self.assertIsInstance(
            self.user.nhs_number,
            str
        )


    def test_has_email_as_a_string(self):
        self.user.email = 'test@example.com'
        self.assertIsInstance(
            self.user.email,
            str
        )


    def test_has_created_at_as_a_datetime(self):
        self.assertIsInstance(
            self.user.created_at,
            datetime
        )

    def test_has_updated_at_as_a_datetime(self):
        self.assertIsInstance(
            self.user.updated_at,
            datetime
        )


    def test_nhs_number_has_a_max_length_of_10(self):
        with self.assertRaises(ValidationError) as context:
            UserFactory(nhs_number="1"*11)

        self.assertIn(
            "Ensure this value has at most 10 characters (it has 11).",
            context.exception.messages
        )

    def test_has_many_response_sets(self):
        response_set = self.user.responseset_set.create(
            have_you_ever_smoked=0,
            date_of_birth=date(2000, 9, 8)
        )
        self.assertIn(response_set, list(self.user.responseset_set.all()))

    def test_raises_a_validation_error_if_nhs_number_is_null(self):
        with self.assertRaises(ValidationError) as context:
            UserFactory(nhs_number=None)

        self.assertIn(
            "This field cannot be null.",
            context.exception.messages
        )


    def test_raises_a_validation_error_if_nhs_number_is_duplicate(self):
        with self.assertRaises(ValidationError) as context:
            UserFactory(nhs_number=self.user.nhs_number)

        self.assertIn(
            "User with this Nhs number already exists.",
            context.exception.messages
        )
