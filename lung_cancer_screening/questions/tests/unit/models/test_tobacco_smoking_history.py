from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory

from ....models.smoking_frequency_response import SmokingFrequencyValues
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ....models.tobacco_smoking_history import TobaccoSmokingHistory

@tag("TypesTobaccoSmoking")
class TestTobaccoSmokingHistory(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


    def test_has_a_valid_factory(self):
        model = TobaccoSmokingHistoryFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set
        )

        self.assertEqual(response.response_set, self.response_set)


    def test_has_type_as_a_string(self):
        response = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            cigarettes=True,
        )

        self.assertIsInstance(response.type, str)


    def test_is_valid_with_a_duplicate_response_set_and_level_with_different_types(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )


    def test_is_valid_with_a_duplicate_response_set_and_type_with_different_levels(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )


    def test_is_invalid_with_a_duplicate_response_set_type_and_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        with self.assertRaises(ValidationError):
            TobaccoSmokingHistoryFactory(
                response_set=self.response_set,
                cigarettes=True,
                level=TobaccoSmokingHistory.Levels.NORMAL,
            )


    def test_is_valid_with_a_duplicate_response_set_with_both_no_change_and_normal_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NO_CHANGE,
        )


    def test_is_invalid_when_no_change_exists_and_creating_a_non_normal_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NO_CHANGE,
        )

        instance = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        with self.assertRaises(ValidationError) as context:
            instance.full_clean()

        self.assertEqual(context.exception.message_dict, {
            "level": ["Cannot have both no change and other levels selected"]
        })


    def test_is_invalid_when_non_normal_level_exists_and_creating_a_no_change(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        instance = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NO_CHANGE,
        )
        with self.assertRaises(ValidationError) as context:
            instance.full_clean()

        self.assertEqual(context.exception.message_dict, {
            "level": ["Cannot have both no change and other levels selected"]
        })


    def test_amount_returns_the_value_of_the_smoked_amount_response(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        SmokedAmountResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=10,
        )
        self.assertEqual(tobacco_smoking_history.amount(), 10)

    def test_amount_returns_none_when_the_smoked_amount_response_does_not_exist(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertIsNone(tobacco_smoking_history.amount())

    def test_frequency_singular_returns_the_value_of_the_smoking_frequency_response(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY,
        )
        self.assertEqual(tobacco_smoking_history.frequency_singular(), "day")

    def test_frequency_singular_returns_none_when_the_smoking_frequency_response_does_not_exist(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertIsNone(tobacco_smoking_history.frequency_singular())

    def test_is_increased_returns_true_when_the_level_is_increased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        self.assertTrue(tobacco_smoking_history.is_increased())

    def test_is_increased_returns_false_when_the_level_is_not_increased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertFalse(tobacco_smoking_history.is_increased())

    def test_is_decreased_returns_true_when_the_level_is_decreased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.DECREASED,
        )
        self.assertTrue(tobacco_smoking_history.is_decreased())

    def test_is_decreased_returns_false_when_the_level_is_not_decreased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertFalse(tobacco_smoking_history.is_decreased())

    def test_is_normal_returns_true_when_the_level_is_normal(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertTrue(tobacco_smoking_history.is_normal())

    def test_is_normal_returns_false_when_the_level_is_not_normal(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        self.assertFalse(tobacco_smoking_history.is_normal())

    def test_grouped_by_type_returns_a_dictionary_of_types_and_their_history(self):
        cigarettes_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        medium_cigars_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        medium_cigars_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        by_type = TobaccoSmokingHistory.objects.grouped_by_type()
        self.assertIn(TobaccoSmokingHistoryTypes.CIGARETTES, by_type)
        self.assertIn(TobaccoSmokingHistoryTypes.MEDIUM_CIGARS, by_type)
        self.assertQuerySetEqual(
            by_type[TobaccoSmokingHistoryTypes.CIGARETTES],
            [cigarettes_normal],
            ordered=False,
        )
        self.assertQuerySetEqual(
            by_type[TobaccoSmokingHistoryTypes.MEDIUM_CIGARS],
            [medium_cigars_normal, medium_cigars_increased],
            ordered=False,
        )

    def test_cigarettes_returns_all_cigarettes_smoking_history_items(self):
        cigarette_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            normal=True,
        )
        cigarette_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
        )

        cigarettes = TobaccoSmokingHistory.objects.cigarettes()

        self.assertIn(cigarette_normal, cigarettes)
        self.assertIn(cigarette_increased, cigarettes)
        self.assertNotIn(medium_cigars, cigarettes)


    def test_small_cigars_returns_all_small_cigars_smoking_history_items(self):
        small_cigar_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            small_cigars=True,
            normal=True,
        )
        small_cigar_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            small_cigars=True,
            increased=True,
        )
        cigarettes = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
        )
        small_cigars = TobaccoSmokingHistory.objects.small_cigars()

        self.assertIn(small_cigar_normal, small_cigars)
        self.assertIn(small_cigar_increased, small_cigars)
        self.assertNotIn(cigarettes, small_cigars)


    def test_medium_cigars_returns_all_medium_cigars_smoking_history_items(self):
        medium_cigar_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            normal=True,
        )
        medium_cigar_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            increased=True,
        )
        cigarettes = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
        )
        medium_cigars = TobaccoSmokingHistory.objects.medium_cigars()

        self.assertIn(medium_cigar_normal, medium_cigars)
        self.assertIn(medium_cigar_increased, medium_cigars)
        self.assertNotIn(cigarettes, medium_cigars)


    def test_large_cigars_returns_all_large_cigars_smoking_history_items(self):
        large_cigar_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            large_cigars=True,
            normal=True,
        )
        large_cigar_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            large_cigars=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
        )

        large_cigars = TobaccoSmokingHistory.objects.large_cigars()

        self.assertIn(large_cigar_normal, large_cigars)
        self.assertIn(large_cigar_increased, large_cigars)
        self.assertNotIn(medium_cigars, large_cigars)


    def test_rolling_tobacco_returns_all_rolling_tobacco_smoking_history_items(self):
        rolling_tobacco_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
            normal=True,
        )
        rolling_tobacco_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
        )

        rolling_tobacco = TobaccoSmokingHistory.objects.rolling_tobacco()

        self.assertIn(rolling_tobacco_normal, rolling_tobacco)
        self.assertIn(rolling_tobacco_increased, rolling_tobacco)
        self.assertNotIn(medium_cigars, rolling_tobacco)


    def test_pipe_returns_all_pipe_smoking_history_items(self):
        pipe_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
            normal=True,
        )
        pipe_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
        )

        pipes = TobaccoSmokingHistory.objects.pipe()

        self.assertIn(pipe_normal, pipes)
        self.assertIn(pipe_increased, pipes)
        self.assertNotIn(medium_cigars, pipes)


    def test_cigarillos_returns_all_cigarillos_smoking_history_items(self):
        cigarillo_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarillos=True,
            normal=True,
        )
        cigarillo_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarillos=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
        )

        cigarillos = TobaccoSmokingHistory.objects.cigarillos()

        self.assertIn(cigarillo_normal, cigarillos)
        self.assertIn(cigarillo_increased, cigarillos)
        self.assertNotIn(medium_cigars, cigarillos)


    def test_url_type_returns_the_url_type_of_the_tobacco_smoking_history(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertEqual(tobacco_smoking_history.url_type(), "rolling-tobacco")


    def test_by_url_type_returns_the_tobacco_smoking_history_by_the_url_type(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertIn(
            tobacco_smoking_history,
            TobaccoSmokingHistory.objects.by_url_type("rolling-tobacco")
        )


    def test_human_type_returns_the_human_type_of_the_tobacco_smoking_history(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertEqual(tobacco_smoking_history.human_type(), "Rolling tobacco")


    def test_human_type_returns_the_human_type_of_the_tobacco_smoking_history_with_a_prefix_when_the_type_is_pipe(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
        )
        self.assertEqual(tobacco_smoking_history.human_type(), "a Pipe")


    def test_unit_returns_the_unit_of_the_tobacco_smoking_history_as_human_type_by_default(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
        )
        self.assertEqual(tobacco_smoking_history.unit(), "cigarettes")


    def test_unit_returns_the_unit_of_the_tobacco_smoking_history_as_grams_of_rolling_tobacco_when_the_type_is_rolling_tobacco(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertEqual(tobacco_smoking_history.unit(), "grams of rolling tobacco")


    def test_unit_returns_the_unit_of_the_tobacco_smoking_history_as_full_pipe_loads_when_the_type_is_pipe(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
        )
        self.assertEqual(tobacco_smoking_history.unit(), "full pipe loads")


    def test_is_pipe_returns_true_when_the_type_is_pipe(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
        )
        self.assertTrue(tobacco_smoking_history.is_pipe())


    def test_is_pipe_returns_false_when_the_type_is_not_pipe(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertFalse(tobacco_smoking_history.is_pipe())


    def test_is_rolling_tobacco_returns_true_when_the_type_is_rolling_tobacco(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            rolling_tobacco=True,
        )
        self.assertTrue(tobacco_smoking_history.is_rolling_tobacco())


    def test_is_rolling_tobacco_returns_false_when_the_type_is_not_rolling_tobacco(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            pipe=True,
        )
        self.assertFalse(tobacco_smoking_history.is_rolling_tobacco())


    def test_is_complete_returns_true_when_the_all_normal_level_responses_are_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            normal=True,
            complete=True
        )

        self.assertTrue(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_when_the_normal_level_current_response_is_not_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            normal=True,
            complete=True
        )
        tobacco_smoking_history.smoking_current_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_when_the_normal_level_smoked_amount_response_is_not_present(
        self,
    ):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, normal=True, complete=True
        )
        tobacco_smoking_history.smoked_amount_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_when_the_normal_level_smoking_frequency_response_is_not_present(
        self,
    ):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, normal=True, complete=True
        )
        tobacco_smoking_history.smoking_frequency_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_when_the_normal_level_smoked_total_years_response_is_not_present(
        self,
    ):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, normal=True, complete=True
        )
        tobacco_smoking_history.smoked_total_years_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_true_for_a_changed_level_when_all_responses_are_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, increased=True, complete=True
        )

        self.assertTrue(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_true_for_a_decreased_level_no_is_current_response_is_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, decreased=True, complete=True
        )
        tobacco_smoking_history.smoking_current_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertTrue(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_for_a_decreased_level_no_smoked_amount_response_is_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, decreased=True, complete=True
        )
        tobacco_smoking_history.smoked_amount_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_for_a_decreased_level_no_smoking_frequency_response_is_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, decreased=True, complete=True
        )
        tobacco_smoking_history.smoking_frequency_response.delete()
        tobacco_smoking_history.refresh_from_db()
        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_false_for_a_decreased_level_no_smoked_total_years_response_is_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, decreased=True, complete=True
        )
        tobacco_smoking_history.smoked_total_years_response.delete()
        tobacco_smoking_history.refresh_from_db()

        self.assertFalse(tobacco_smoking_history.is_complete())


    def test_is_complete_returns_true_for_a_no_change_level_when_no_responses_are_present(self):
        AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set,
        )
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set, no_change=True
        )

        self.assertTrue(tobacco_smoking_history.is_complete())


    def test_in_form_order_returns_the_tobacco_smoking_history_in_form_order(self):
        cigarettes_decreased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            decreased=True,
        )
        medium_cigars_decreased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            decreased=True,
        )
        cigarettes_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            normal=True,
        )
        medium_cigars_increased = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            increased=True,
        )
        medium_cigars_normal = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            medium_cigars=True,
            normal=True,
        )

        in_form_order = TobaccoSmokingHistory.objects.in_form_order()
        self.assertQuerySetEqual(
            in_form_order,
            [cigarettes_normal, cigarettes_decreased, medium_cigars_normal, medium_cigars_increased, medium_cigars_decreased],
            ordered=True,
        )


    def test_user_editable_does_not_include_no_change(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarillos=True,
            no_change=True,
        )
        self.assertQuerySetEqual(
            TobaccoSmokingHistory.objects.user_editable().all(),
            [],
        )
