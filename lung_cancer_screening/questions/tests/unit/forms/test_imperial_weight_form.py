from django.test import TestCase

from ....models.participant import Participant
from ....forms.imperial_weight_form import ImperialWeightForm

class TestImperialWeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")
        self.response_set = self.participant.responseset_set.create(
            weight_metric=1704
        )

    def test_is_valid_with_valid_input(self):
        form = ImperialWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid())

    def test_converts_stone_and_pounds_to_kilograms_integer(self):
        form = ImperialWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        self.assertEqual(form.cleaned_data['weight_imperial'], 79)

    def test_setting_weight_imperial_clears_weight_metric(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            participant=self.participant,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )
        form.save()
        self.assertEqual(self.response_set.weight_metric, None)

    def test_is_invalid_with_missing_data(self):
        form = ImperialWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",
                # missing pounds
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Enter your weight"]
        )

    def test_is_invalid_when_given_a_decimal_stone_value(self):
        form = ImperialWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_imperial_0": "5.2",
                "weight_imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Stone must be in whole numbers"]
        )
