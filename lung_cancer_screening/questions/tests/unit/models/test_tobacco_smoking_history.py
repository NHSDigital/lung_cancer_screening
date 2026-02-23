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
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
        )

        self.assertIsInstance(response.type, str)


    def test_is_valid_with_a_duplicate_response_set_and_level_with_different_types(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARS,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )


    def test_is_valid_with_a_duplicate_response_set_and_type_with_different_levels(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )


    def test_is_invalid_with_a_duplicate_response_set_type_and_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        with self.assertRaises(ValidationError):
            TobaccoSmokingHistoryFactory(
                response_set=self.response_set,
                type=TobaccoSmokingHistoryTypes.CIGARETTES,
                level=TobaccoSmokingHistory.Levels.NORMAL,
            )


    def test_is_valid_with_a_duplicate_response_set_with_both_no_change_and_normal_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NO_CHANGE,
        )


    def test_is_invalid_when_no_change_exists_and_creating_a_non_normal_level(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NO_CHANGE,
        )

        instance = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
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
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        instance = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
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
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
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
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertIsNone(tobacco_smoking_history.amount())

    def test_frequency_singular_returns_the_value_of_the_smoking_frequency_response(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
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
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertIsNone(tobacco_smoking_history.frequency_singular())

    def test_is_increased_returns_true_when_the_level_is_increased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        self.assertTrue(tobacco_smoking_history.is_increased())

    def test_is_increased_returns_false_when_the_level_is_not_increased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertFalse(tobacco_smoking_history.is_increased())

    def test_is_decreased_returns_true_when_the_level_is_decreased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.DECREASED,
        )
        self.assertTrue(tobacco_smoking_history.is_decreased())

    def test_is_decreased_returns_false_when_the_level_is_not_decreased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertFalse(tobacco_smoking_history.is_decreased())

    def test_is_normal_returns_true_when_the_level_is_normal(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        self.assertTrue(tobacco_smoking_history.is_normal())

    def test_is_normal_returns_false_when_the_level_is_not_normal(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        self.assertFalse(tobacco_smoking_history.is_normal())
