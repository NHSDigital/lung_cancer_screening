from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ....models.tobacco_smoking_history import (
    TobaccoSmokingHistoryTypes,
)
from ....forms.types_tobacco_smoking_form import TypesTobaccoSmokingForm


@tag("TypesTobaccoSmoking")
class TestTypesTobaccoSmokingForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


    def test_is_valid_a_valid_value(self):
        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": [TobaccoSmokingHistoryTypes.CIGARETTES]
            }
        )
        self.assertTrue(form.is_valid())


    def test_is_invalid_with_an_invalid_value(self):
        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": ["invalid"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )


    def test_is_invalid_when_no_option_is_selected(self):
        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": []
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select the type of tobacco you smoke or have smoked"],
        )

    def test_saves_an_tobacco_smoking_type_for_each_value_selected(self):
        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": [
                    TobaccoSmokingHistoryTypes.CIGARETTES,
                    TobaccoSmokingHistoryTypes.PIPE
                ]
            }
        )

        form.save()
        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 2)
        self.assertEqual(self.response_set.tobacco_smoking_history.first().type, TobaccoSmokingHistoryTypes.CIGARETTES)
        self.assertEqual(self.response_set.tobacco_smoking_history.last().type, TobaccoSmokingHistoryTypes.PIPE)


    def test_does_not_create_a_new_tobacco_smoking_type_if_it_already_exists(self):
        TobaccoSmokingHistoryFactory(response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES)

        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": [TobaccoSmokingHistoryTypes.CIGARETTES]
            }
        )
        form.save()
        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 1)
        self.assertEqual(self.response_set.tobacco_smoking_history.first().type, TobaccoSmokingHistoryTypes.CIGARETTES)


    def test_deletes_a_tobacco_smoking_type_if_it_is_no_longer_selected(self):
        TobaccoSmokingHistoryFactory(response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES)

        form = TypesTobaccoSmokingForm(
            response_set=self.response_set,
            data={
                "value": [TobaccoSmokingHistoryTypes.PIPE]
            }
        )
        form.save()
        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 1)
        self.assertNotIn(
            TobaccoSmokingHistoryTypes.CIGARETTES,
            self.response_set.tobacco_smoking_history.values_list('type', flat=True)
        )
