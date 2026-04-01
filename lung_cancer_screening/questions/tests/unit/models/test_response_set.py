from django.test import TestCase, tag
from datetime import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError

from ...factories.user_factory import UserFactory
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.terms_of_use_response_factory import TermsOfUseResponseFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.check_need_appointment_response_factory import CheckNeedAppointmentResponseFactory
from ...factories.when_you_quit_smoking_response_factory import WhenYouQuitSmokingResponseFactory

from ....models.user import User
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
from ....models.have_you_ever_smoked_response import HaveYouEverSmokedValues

from ....models.response_set import ResponseSet

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


    def test_saving_a_submitted_response_set_does_not_included_itself_in_unsubmitted_response_sets_validation(self):
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


    def test_is_complete_returns_true_if_current_smoker_and_when_you_quit_smoking_is_incomplete(self):
        response_set = ResponseSetFactory.create(complete=True)
        response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=response_set,
            current_smoker=True
        )

        self.assertTrue(response_set.is_complete())


    def test_is_complete_returns_true_if_former_smoker_and_when_you_quit_smoking_is_complete(self):
        response_set = ResponseSetFactory.create(complete=True)
        response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=response_set,
            former_smoker=True
        )
        WhenYouQuitSmokingResponseFactory.create(
            response_set=response_set,
            value=response_set.age_when_started_smoking_response.value + 1,
        )

        self.assertTrue(response_set.is_complete())


    def test_is_complete_returns_false_if_former_smoker_and_when_you_quit_smoking_is_incomplete(self):
        response_set = ResponseSetFactory.create(complete=True)
        response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=response_set,
            former_smoker=True
        )

        self.assertFalse(response_set.is_complete())


    def test_is_ineligible_returns_false_when_any_eligibility_question_is_not_answered(self):
        response_set = ResponseSetFactory.create()

        self.assertFalse(response_set.is_eligible())


    def test_is_eligible_returns_true_when_smoked_age_and_need_appointment_are_eligible(self):
        TermsOfUseResponseFactory.create(
            response_set=self.response_set,
            value=True
        )

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


    def test_is_ineligible_returns_false_when_smoking_is_ineligible(self):
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


    def test_is_ineligible_returns_false_when_age_is_ineligible(self):
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


    def test_is_ineligible_returns_false_when_need_appointment_is_ineligible(self):
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


    def test_types_tobacco_smoking_history_returns_all_types_of_tobacco_smoking_history_without_duplicate_types(self):
        cigarettes = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            increased=True,
        )
        cigarillos = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        self.assertEqual(
            list(self.response_set.types_tobacco_smoking_history()),
            [cigarettes.type.value, cigarillos.type.value]
        )


    def test_previous_normal_smoking_history_returns_none_when_it_is_the_only_smoking_history_item    (self):
        self.response_set.tobacco_smoking_history.all().delete()
        smoking_history_item = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set
        )
        self.assertIsNone(
            self.response_set.previous_normal_smoking_history(
                smoking_history_item
            )
        )


    def test_previous_normal_smoking_history_returns_none_when_it_is_the_first_smoking_history_item_respecting_form_order(self):
        self.response_set.tobacco_smoking_history.all().delete()
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        smoking_history_item = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
        )
        self.assertIsNone(
            self.response_set.previous_normal_smoking_history(
                smoking_history_item
            )
        )


    def test_previous_normal_smoking_history_returns_the_previous_normal_smoking_history_when_it_is_not_the_only_smoking_history_item(self):
        self.response_set.tobacco_smoking_history.all().delete()
        previous_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True
        )
        smoking_history_item = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True
        )
        self.assertEqual(
            self.response_set.previous_normal_smoking_history(smoking_history_item),
            previous_normal_smoking_history
        )


    def test_previous_smoking_history_returns_none_when_it_is_the_only_smoking_history_item(self):
        self.response_set.tobacco_smoking_history.all().delete()
        smoking_history_item = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set
        )
        self.assertIsNone(
            self.response_set.previous_smoking_history(smoking_history_item)
        )


    def test_returns_the_increased_smoking_history_when_it_is_attached_to_the_previous_normal_history(self):
        self.response_set.tobacco_smoking_history.all().delete()
        previous_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True
        )
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=previous_normal_smoking_history.type,
            increased=True
        )
        current_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        self.assertEqual(
            self.response_set.previous_smoking_history(current_normal_smoking_history),
            increased_smoking_history
        )

    def test_returns_the_decreased_smoking_history_when_it_is_attached_to_the_previous_normal_history(self):
        self.response_set.tobacco_smoking_history.all().delete()
        previous_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True
        )
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=previous_normal_smoking_history.type,
            decreased=True
        )
        current_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        self.assertEqual(
            self.response_set.previous_smoking_history(current_normal_smoking_history),
            decreased_smoking_history
        )

    def test_returns_decreased_when_the_previous_normal_smoking_history_when_both_previous_and_current_exist(self):
        self.response_set.tobacco_smoking_history.all().delete()
        previous_normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True
        )
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=previous_normal_smoking_history.type,
            decreased=True
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=previous_normal_smoking_history.type,
            increased=True
        )
        current_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        self.assertEqual(
            self.response_set.previous_smoking_history(current_smoking_history),
            decreased_smoking_history
        )


    def test_next_smoking_history_returns_none_when_it_is_the_only_smoking_history_item(self):
        smoking_history_item = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set
        )
        self.assertIsNone(
            self.response_set.next_smoking_history(smoking_history_item)
        )


    def test_next_smoking_history_returns_the_next_smoking_history_when_it_is_not_the_only_smoking_history_item_respecting_form_order(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
            increased=True,
        )
        next_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
        )
        current_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
        )
        self.assertEqual(
            self.response_set.next_smoking_history(current_smoking_history),
            next_smoking_history
        )


    def test_next_smoking_history_does_not_include_no_change(self):
        current_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
            normal=True,
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
            no_change=True,
        )
        self.assertIsNone(
            self.response_set.next_smoking_history(current_smoking_history)
        )


    def test_current_smoker_returns_true_when_the_user_is_currently_smoking(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value,
        )
        self.assertTrue(self.response_set.current_smoker())


    def test_current_smoker_returns_false_when_the_user_is_not_currently_smoking(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value,
        )
        self.assertFalse(self.response_set.current_smoker())


    def test_current_smoker_returns_none_when_the_has_not_answered_the_question(self):
        self.assertIsNone(self.response_set.current_smoker())


    def test_former_smoker_returns_true_when_the_user_is_a_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value,
        )
        self.assertTrue(self.response_set.former_smoker())


    def test_former_smoker_returns_false_when_the_user_is_not_a_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value,
        )
        self.assertFalse(self.response_set.former_smoker())


    def test_former_smoker_returns_none_when_the_has_not_answered_the_question(self):
        self.assertIsNone(self.response_set.former_smoker())
