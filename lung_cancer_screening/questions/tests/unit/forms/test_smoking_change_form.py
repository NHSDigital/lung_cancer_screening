from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistory, TobaccoSmokingHistoryTypes
from ....forms.smoking_change_form import SmokingChangeForm


@tag("SmokingChange")
class TestSmokingChangeForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create(complete_without_smoking=True)
        self.normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            normal=True,
            complete=True
        )
        self.smoking_current_response = self.normal_smoking_history.smoking_current_response


    def test_is_valid_a_valid_value(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={"value": [TobaccoSmokingHistory.Levels.INCREASED]}
        )
        self.assertTrue(form.is_valid())


    def test_is_invalid_with_an_invalid_value(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={"value": ["invalid"]}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )


    def test_has_a_required_validation_error_for_current_smoker(self):
        self.smoking_current_response.value = True
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={"value": []}
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if the number of cigarettes you smoke has changed over time"],
        )


    def test_has_a_required_validation_error_for_previous_smoker(self):
        self.smoking_current_response.value = False
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={"value": []}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if the number of cigarettes you smoked has changed over time"],
        )


    def test_saves_an_tobacco_smoking_history_for_the_type_and_level_selected(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [
                    TobaccoSmokingHistory.Levels.INCREASED,
                    TobaccoSmokingHistory.Levels.DECREASED,
                ]
            }
        )

        form.save()

        items = self.response_set.tobacco_smoking_history
        self.assertEqual(items.count(), 3)  # Normal, Increased and Decreased
        self.assertTrue(all([
            item.type == self.normal_smoking_history.type
            for item in items.all()
        ]))


    def test_does_not_create_a_new_tobacco_smoking_history_if_the_level_already_exists(self):
        existing_item = TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [TobaccoSmokingHistory.Levels.INCREASED]
            }
        )
        form.save()
        increased_history_items = self.response_set.tobacco_smoking_history.filter(level=TobaccoSmokingHistory.Levels.INCREASED)
        self.assertEqual(increased_history_items.count(), 1)
        self.assertEqual(
            increased_history_items.first(),
            existing_item
        )


    def test_deletes_a_tobacco_smoking_history_if_the_level_is_no_longer_selected(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [TobaccoSmokingHistory.Levels.NO_CHANGE]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.INCREASED
        ).count(), 0)


    def test_does_not_delete_normal_level_smoking_history(self):
        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [TobaccoSmokingHistory.Levels.NO_CHANGE]
            }
        )
        form.save()

        self.assertEqual(self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).count(), 1)


    def test_prevents_both_no_change_and_other_levels_selected_when_current_smoker(self):
        self.smoking_current_response.value = True
        self.smoking_current_response.save()

        self.normal_smoking_history.type = TobaccoSmokingHistoryTypes.ROLLING_TOBACCO.value
        self.normal_smoking_history.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [
                    TobaccoSmokingHistory.Levels.NO_CHANGE,
                    TobaccoSmokingHistory.Levels.INCREASED
                ]
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if the number of grams of rolling tobacco you smoke has changed over time, or select 'no, it has not changed'"],
        )


    def test_prevents_both_no_change_and_other_levels_selected_when_previous_smoker(self):
        self.smoking_current_response.value = False
        self.smoking_current_response.save()

        self.normal_smoking_history.type = TobaccoSmokingHistoryTypes.ROLLING_TOBACCO.value
        self.normal_smoking_history.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": [
                    TobaccoSmokingHistory.Levels.NO_CHANGE,
                    TobaccoSmokingHistory.Levels.INCREASED
                ]
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if the number of grams of rolling tobacco you smoked has changed over time, or select 'no, it has not changed'"],
        )


    def test_initializes_the_form_based_on_existing_smoking_histories(self):
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        TobaccoSmokingHistoryFactory(
            response_set=self.response_set,
            cigarettes=True,
            level=TobaccoSmokingHistory.Levels.DECREASED,
        )

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
        )

        initial = form.fields["value"].initial
        self.assertIn(TobaccoSmokingHistory.Levels.INCREASED, initial)
        self.assertIn(TobaccoSmokingHistory.Levels.DECREASED, initial)


    def test_has_a_label_for_current_smoker_with_type(self):
        self.smoking_current_response.value = True
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
        )

        self.assertEqual(
            form.fields["value"].label,
            "Has the number of cigarettes you normally smoke changed over time?"
        )

    def test_has_a_label_for_previous_smoker_with_type(self):
        self.smoking_current_response.value = False
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
        )

        self.assertEqual(
            form.fields["value"].label,
            "Did the number of cigarettes you normally smoke change over time?"
        )

    def test_has_correct_page_title_for_current_smoking_change(self):
        self.smoking_current_response.value = True
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
        )

        self.assertEqual(
            form.page_title(),
            "Has the number of cigarettes you smoke changed over time?"
        )

    def test_has_correct_page_title_for_previous_smoking_change(self):
        self.smoking_current_response.value = False
        self.smoking_current_response.save()

        form = SmokingChangeForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
        )

        self.assertEqual(
            form.page_title(),
            "Did the number of cigarettes you smoke change over time?"
        )

