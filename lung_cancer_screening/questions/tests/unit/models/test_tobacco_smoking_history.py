from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
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
