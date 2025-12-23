from django import forms

from ...nhsuk_forms.imperial_height_field import ImperialHeightField
from ..models.height_response import HeightResponse


class ImperialHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["imperial"] = ImperialHeightField(
            label="Height",
            required=True,
            require_all_fields=False,
            error_messages={
                'required': 'Enter your height',
            }
        )

    def clean_metric(self):
        return None

    class Meta:
        model = HeightResponse
        fields = ['imperial', 'metric']
