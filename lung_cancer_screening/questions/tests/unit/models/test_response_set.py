from django.test import TestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django.core.exceptions import ValidationError

from ...factories.user_factory import UserFactory
from ...factories.response_set_factory import ResponseSetFactory
from ....models.user import User
from ....models.response_set import ResponseSet

class TestResponseSet(TestCase):
    def setUp(self):
        user = UserFactory()
        self.response_set = user.responseset_set.create()

    # FIELDS

    def test_has_a_user_as_a_foreign_key(self):
        self.assertIsInstance(
            self.response_set.user,
            User
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

    # VALIDATIONS

    def test_is_invalid_if_another_unsubmitted_response_set_exists(self):
        user = UserFactory()
        user.responseset_set.create(submitted_at=None)

        with self.assertRaises(ValidationError) as context:
            user.responseset_set.create(submitted_at=None)

        self.assertEqual(
            context.exception.messages[0],
            "An unsubmitted response set already exists for this user"
        )

    def test_is_invalid_if_another_response_set_was_submitted_within_the_last_year(self):
        user = UserFactory()
        user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        with self.assertRaises(ValidationError) as context:
            user.responseset_set.create()

        self.assertEqual(
            context.exception.messages[0],
            "Responses have already been submitted for this user"
        )

# Query managers
    def test_objects_returns_all_response_sets(self):
        unsubmitted_response_set = ResponseSetFactory()
        submitted_response_set = ResponseSetFactory(submitted_at=timezone.now())

        response_sets = ResponseSet.objects.all()
        self.assertIn(
            unsubmitted_response_set,
            response_sets,
        )
        self.assertIn(
            submitted_response_set,
            response_sets,
        )

    def test_unsubmitted_returns_only_unsubmitted_response_sets(self):
        unsubmitted_response_set = ResponseSetFactory()
        submitted_response_set = ResponseSetFactory(submitted_at=timezone.now())

        unsubmitted_response_sets = ResponseSet.objects.unsubmitted().all()
        self.assertIn(
            unsubmitted_response_set,
            unsubmitted_response_sets,
        )
        self.assertNotIn(
            submitted_response_set,
            unsubmitted_response_sets,
        )

    def test_submitted_returns_only_submitted_response_sets(self):
        unsubmitted_response_set = ResponseSetFactory()
        submitted_response_set = ResponseSetFactory(submitted_at=timezone.now() - relativedelta(years=1))

        submitted_response_sets = ResponseSet.objects.submitted().all()
        self.assertIn(
            submitted_response_set,
            submitted_response_sets,
        )
        self.assertNotIn(
            unsubmitted_response_set,
            submitted_response_sets,
        )

    def test_submitted_in_last_year_returns_only_submitted_response_sets_in_the_last_year(self):
        submitted_response_set_in_last_year = ResponseSetFactory(
            submitted_at=timezone.now() - relativedelta(days=364)
        )
        submitted_response_set_older_than_last_year = ResponseSetFactory(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        submitted_response_sets_in_last_year = ResponseSet.objects.submitted_in_last_year().all()
        self.assertIn(
            submitted_response_set_in_last_year,
            submitted_response_sets_in_last_year,
        )
        self.assertNotIn(
            submitted_response_set_older_than_last_year,
            submitted_response_sets_in_last_year,
        )
