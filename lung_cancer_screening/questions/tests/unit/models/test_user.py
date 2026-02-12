from datetime import datetime
from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.user_factory import UserFactory


@tag("User")
class TestUser(TestCase):
    def setUp(self):
        self.user = UserFactory()


    def test_has_a_valid_factory(self):
        model = UserFactory.build()
        model.full_clean()


    def test_has_sub_as_a_string(self):
        self.assertIsInstance(self.user.sub, str)

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


    def test_has_many_response_sets(self):
        response_set = self.user.responseset_set.create()
        self.assertIn(response_set, list(self.user.responseset_set.all()))


    def test_is_invalid_without_a_sub(self):
        self.user.sub = None

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

        self.assertIn(
            "This field cannot be null.",
            context.exception.messages
        )

    def test_in_invalid_if_sub_is_not_unique(self):
        with self.assertRaises(ValidationError) as context:
            UserFactory(sub=self.user.sub)

        self.assertIn(
            "User with this Sub already exists.",
            context.exception.messages
        )


    def test_is_invalid_without_nhs_number(self):
        self.user.nhs_number = None

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

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


    def test_nhs_number_has_a_max_length_of_10(self):
        self.user.nhs_number = "1"*11

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

        self.assertIn(
            "Ensure this value has at most 10 characters (it has 11).",
            context.exception.messages
        )


    def test_is_invalid_without_a_given_name(self):
        self.user.given_name = None

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

        self.assertIn(
            "This field cannot be null.",
            context.exception.messages
        )

    def test_is_invalid_without_a_family_name(self):
        self.user.family_name = None

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

        self.assertIn(
            "This field cannot be null.",
            context.exception.messages[0]
        )


    def test_is_invalid_without_an_email(self):
        self.user.email = None

        with self.assertRaises(ValidationError) as context:
            self.user.full_clean()

        self.assertIn(
            "This field cannot be null.",
            context.exception.messages[0]
        )


    def test_has_recently_submitted_responses_returns_true_if_has_recently_submitted_response_set(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )
        self.assertTrue(self.user.has_recently_submitted_responses())


    def test_has_recently_submitted_responses_returns_false_if_has_no_recently_submitted_response_set(self):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )
        self.assertFalse(self.user.has_recently_submitted_responses())


    def test_full_name_returns_the_full_name(self):
        self.user.given_name = "John"
        self.user.family_name = "Doe"
        self.assertEqual(self.user.full_name, "John Doe")
