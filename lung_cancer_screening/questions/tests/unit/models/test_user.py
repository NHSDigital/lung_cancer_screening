from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError

from ....models.user import User


class TestUser(TestCase):
    def setUp(self):
        self.nhs_number = "1234567890"
        self.user = User.objects.create_user(self.nhs_number)

    def test_has_nhs_number_as_a_string(self):
        self.assertIsInstance(
            self.user.nhs_number,
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
            User.objects.create_user("1"*11)

        self.assertIn(
            "Ensure this value has at most 10 characters (it has 11).",
            context.exception.messages
        )

    def test_raises_a_value_error_if_nhs_number_is_null(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None)

    def test_raises_a_validation_error_if_nhs_number_is_duplicate(self):
        with self.assertRaises(ValidationError) as context:
            User.objects.create_user(self.nhs_number)

        self.assertIn(
            "User with this Nhs number already exists.",
            context.exception.messages
        )
