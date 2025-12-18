from django.test import TestCase
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django.core.exceptions import ValidationError

from ...factories.user_factory import UserFactory
from ...factories.response_set_factory import ResponseSetFactory
from ....models.user import User
from ....models.response_set import ResponseSet, HaveYouEverSmokedValues, SexAtBirthValues, GenderValues, EthnicityValues

class TestResponseSet(TestCase):
    def setUp(self):
        user = UserFactory()
        self.response_set = user.responseset_set.create()

    # FIELDS

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

    def test_has_height_metric_as_a_int(self):
        self.response_set.height_metric = 1700
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.height_metric,
            int
        )

    def test_has_an_imperial_height_as_a_int(self):
        self.response_set.height_imperial = 68
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.height_imperial,
            int
        )

    def test_has_an_metric_weight_as_a_int(self):
        self.response_set.weight_metric = 680
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.weight_metric,
            int
        )

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

    def test_has_sex_at_birth_as_string(self):
        self.response_set.sex_at_birth = SexAtBirthValues.MALE
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.sex_at_birth,
            str
        )

    def test_has_gender_as_string(self):
        self.response_set.gender = GenderValues.MALE
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.gender,
            str
        )

    def test_has_ethnicity_as_string(self):
        self.response_set.ethnicity = EthnicityValues.WHITE
        self.response_set.save()

        self.assertIsInstance(
            self.response_set.ethnicity,
            str
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

    def test_is_invalid_if_height_is_below_lower_bound(self):
        self.response_set.height_metric = ResponseSet.MIN_HEIGHT_METRIC - 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages
        )

    def test_is_invalid_if_height_is_above_upper_bound(self):
        self.response_set.height_metric = ResponseSet.MAX_HEIGHT_METRIC + 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages
        )

    def test_is_invalid_if_imperial_height_is_below_lower_bound(self):
        self.response_set.height_imperial = ResponseSet.MIN_HEIGHT_IMPERIAL - 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 4 feet 7 inches and 8 feet",
            context.exception.messages
        )

    def test_is_invalid_if_imperial_height_is_above_upper_bound(self):
        self.response_set.height_imperial = ResponseSet.MAX_HEIGHT_IMPERIAL + 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Height must be between 4 feet 7 inches and 8 feet",
            context.exception.messages
        )

    def test_formatted_height_returns_height_in_cm_if_set(self):
        self.response_set.height_metric = 1701
        self.response_set.save()

        self.assertEqual(
            self.response_set.formatted_height,
            "170.1cm"
        )

    def test_formatted_height_returns_imperial_height_if_set(self):
        self.response_set.height_imperial = 68
        self.response_set.save()

        self.assertEqual(
            self.response_set.formatted_height,
            "5 feet 8 inches"
        )

    def test_is_invalid_if_weight_metric_is_below_lower_bound(self):
        self.response_set.weight_metric = ResponseSet.MIN_WEIGHT_METRIC - 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Weight must be between 25.4kg and 317.5kg",
            context.exception.messages
        )

    def test_is_invalid_if_weight_metric_is_above_upper_bound(self):
        self.response_set.weight_metric = ResponseSet.MAX_WEIGHT_METRIC + 1

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertIn(
            "Weight must be between 25.4kg and 317.5kg",
            context.exception.messages
        )

    def test_is_valid_if_sex_at_birth_is_null(self):
        self.response_set.sex_at_birth = None
        self.response_set.save()

        self.assertIsNone(
            self.response_set.sex_at_birth
        )


    def test_is_invalid_if_sex_at_birth_is_not_an_accepted_value(self):
        self.response_set.sex_at_birth = "X"

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "Value 'X' is not a valid choice."
        )

    def test_is_valid_if_gender_is_null(self):
        self.response_set.gender = None
        self.response_set.save()

        self.assertIsNone(
            self.response_set.gender
        )

    def test_is_invalid_if_gender_is_not_an_accepted_value(self):
        self.response_set.gender = "X"

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "Value 'X' is not a valid choice."
        )

    def test_is_valid_if_ethnicity_is_null(self):
        self.response_set.ethnicity = None
        self.response_set.save()

        self.assertIsNone(
            self.response_set.ethnicity
        )

    def test_is_invalid_if_ethnicity_is_not_an_accepted_value(self):
        self.response_set.ethnicity = "X"

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "Value 'X' is not a valid choice."
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
