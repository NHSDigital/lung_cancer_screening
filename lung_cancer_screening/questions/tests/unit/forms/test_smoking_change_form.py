from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistory, TobaccoSmokingHistoryTypes
from ....forms.smoking_change_form import SmokingChangeForm


@tag("SmokingChange")
class TestSmokingChangeForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create()


    def test_is_valid_a_valid_value(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={"value": [TobaccoSmokingHistory.Levels.INCREASED]}
        )
        self.assertTrue(form.is_valid())


    def test_is_invalid_with_an_invalid_value(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={"value": ["invalid"]}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )


    def test_is_invalid_when_no_option_is_selected(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={"value": []}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if the number of cigarettes you smoke has changed over time"],
        )


    def test_saves_an_tobacco_smoking_history_for_the_type_and_level_selected(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={
                "value": [
                    TobaccoSmokingHistory.Levels.INCREASED,
                    TobaccoSmokingHistory.Levels.DECREASED,
                ]
            }
        )

        form.save()

        items = self.response_set.tobacco_smoking_history
        self.assertEqual(items.count(), 2)
        self.assertTrue(all([
            item.type == TobaccoSmokingHistoryTypes.CIGARETTES
            for item in items.all()
        ]))


    def test_does_not_create_a_new_tobacco_smoking_history_if_the_level_already_exists(self):
        existing_item = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={
                "value": [TobaccoSmokingHistory.Levels.INCREASED]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 1)
        self.assertEqual(
            self.response_set.tobacco_smoking_history.first(),
            existing_item
        )


    def test_deletes_a_tobacco_smoking_history_if_the_level_is_no_longer_selected(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={
                "value": [TobaccoSmokingHistory.Levels.NO_CHANGE]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.INCREASED
        ).count(), 0)


    def test_does_not_delete_normal_level_smoking_history(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={
                "value": [TobaccoSmokingHistory.Levels.NO_CHANGE]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).count(), 1)

    def test_prevents_both_no_change_and_other_levels_selected(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
            data={
                "value": [TobaccoSmokingHistory.Levels.NO_CHANGE, TobaccoSmokingHistory.Levels.INCREASED]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).count(), 1)
        self.assertEqual(self.response_set.tobacco_smoking_history.all().count(), 1)

    def test_initializes_the_form_based_on_existing_smoking_histories(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.DECREASED,
        )
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
            level=TobaccoSmokingHistory.Levels.STOPPED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_type=TobaccoSmokingHistoryTypes.CIGARETTES,
        )

        self.assertEqual(form.fields["value"].initial, [
            TobaccoSmokingHistory.Levels.INCREASED,
            TobaccoSmokingHistory.Levels.DECREASED,
            TobaccoSmokingHistory.Levels.STOPPED,
        ])
