from django import forms

from ...nhsuk_forms.imperial_weight_field import ImperialWeightField
from ..models.response_set import ResponseSet


class ImperialWeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["weight_imperial"] = ImperialWeightField(
            label="Weight",
            required=True,
            require_all_fields=False,
            error_messages={
                'required': 'Enter your weight'
            }
        )

    def clean_weight_metric(self):
        return None

    class Meta:
        model = ResponseSet
        fields = ['weight_imperial', 'weight_metric']
