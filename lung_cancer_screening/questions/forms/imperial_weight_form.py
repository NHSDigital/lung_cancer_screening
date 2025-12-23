from django import forms

from ...nhsuk_forms.imperial_weight_field import ImperialWeightField
from ..models.weight_response import WeightResponse


class ImperialWeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["imperial"] = ImperialWeightField(
            label="Weight",
            required=True,
            require_all_fields=False,
            error_messages={
                'required': 'Enter your weight'
            }
        )

    def clean_metric(self):
        return None

    class Meta:
        model = WeightResponse
        fields = ['imperial', 'metric']
