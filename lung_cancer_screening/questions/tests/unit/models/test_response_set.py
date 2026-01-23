from django.test import TestCase, tag
from datetime import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError

from ...factories.user_factory import UserFactory
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.check_need_appointment_response_factory import CheckNeedAppointmentResponseFactory
from ....models.user import User
from ....models.response_set import ResponseSet
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues


@tag("ResponseSet")
class TestResponseSet(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSetFactory(user=self.user)


    def test_has_a_valid_factory(self):
        model = ResponseSetFactory.build(user=UserFactory())
        model.full_clean()


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

    def test_is_invalid_if_another_response_set_was_submitted_within_the_recently_submitted_period(self):
        response_set = ResponseSetFactory.create(recently_submitted=True)

        with self.assertRaises(ValidationError) as context:
            response_set.user.responseset_set.create()

        self.assertEqual(
            context.exception.messages[0],
            "Responses have already been submitted for this user"
        )


    def test_Saving_a_submitted_response_Set_does_not_included_itself_in_unsubmitted_response_sets_validation(self):
        response_set = ResponseSetFactory.create(complete=True)
        response_set.submitted_at = timezone.now()

        response_set.full_clean()


    def test_submitted_response_set_is_invalid_if_incomplete(self):
        self.response_set.submitted_at = timezone.now()

        with self.assertRaises(ValidationError) as context:
            self.response_set.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "Response set must be complete before it can be submitted"
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
        submitted_response_set = ResponseSetFactory(recently_submitted=True)

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
        submitted_response_set = ResponseSetFactory(not_recently_submitted=True)

        submitted_response_sets = ResponseSet.objects.submitted().all()
        self.assertIn(
            submitted_response_set,
            submitted_response_sets,
        )
        self.assertNotIn(
            unsubmitted_response_set,
            submitted_response_sets,
        )

    def test_submitted_recently_returns_only_submitted_response_sets_in_the_recently_submitted_period(self):
        recently_submitted_response = ResponseSetFactory(
            recently_submitted=True
        )
        old_submitted_response = ResponseSetFactory(
            not_recently_submitted=True
        )

        recently_submitted_response_sets = ResponseSet.objects.recently_submitted().all()
        self.assertIn(
            recently_submitted_response,
            recently_submitted_response_sets,
        )
        self.assertNotIn(
            old_submitted_response,
            recently_submitted_response_sets,
        )


    def test_is_complete_returns_true_if_all_questions_are_answered(self):
        response_set = ResponseSetFactory.create(complete=True)

        self.assertTrue(response_set.is_complete())


    def test_is_complete_returns_false_if_a_single_question_is_not_answered(self):
        response_set = ResponseSetFactory.create(complete=True)
        response_set.asbestos_exposure_response.delete()
        response_set.refresh_from_db()

        self.assertFalse(response_set.is_complete())


    def test_is_complete_returns_true_if_family_history_cancer_no_and_none_age_diagnosed(self):
        response_set = ResponseSetFactory.create(complete=True)

        family_history = response_set.family_history_lung_cancer
        family_history.value = FamilyHistoryLungCancerValues.NO
        family_history.save()

        response_set.refresh_from_db()

        self.assertTrue(response_set.is_complete())


    def test_is_ineligble_returns_false_when_any_eligibility_question_is_not_answered(self):
        response_set = ResponseSetFactory.create()

        self.assertFalse(response_set.is_eligible())


    def test_is_eligble_returns_true_when_smoked_age_and_need_appointment_are_eligible(self):
        HaveYouEverSmokedResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        CheckNeedAppointmentResponseFactory(
            response_set=self.response_set,
            eligible=True
        )

        self.assertTrue(self.response_set.is_eligible())


    def test_is_ineligble_returns_false_when_smoking_is_inelgible(self):
        HaveYouEverSmokedResponseFactory(
            response_set=self.response_set,
            ineligible=True
        )
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        CheckNeedAppointmentResponseFactory(
            response_set=self.response_set,
            eligible=True
        )

        self.assertFalse(self.response_set.is_eligible())


    def test_is_ineligble_returns_false_when_age_is_inelgible(self):
        HaveYouEverSmokedResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            ineligible=True
        )
        CheckNeedAppointmentResponseFactory(
            response_set=self.response_set,
            eligible=True
        )

        self.assertFalse(self.response_set.is_eligible())


    def test_is_ineligble_returns_false_when_need_appointment_is_inelgible(self):
        HaveYouEverSmokedResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        CheckNeedAppointmentResponseFactory(
            response_set=self.response_set,
            ineligible=True
        )

        self.assertFalse(self.response_set.is_eligible())
