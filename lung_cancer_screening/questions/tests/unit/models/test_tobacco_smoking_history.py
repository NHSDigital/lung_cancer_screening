from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

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
