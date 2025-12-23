from django import forms

from ...nhsuk_forms.decimal_field import DecimalField
from ..models.weight_response import WeightResponse


class MetricWeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert hundreds of grams to kg for display
        if self.instance and self.instance.metric is not None:
            self.initial['metric'] = self.instance.metric / 10

        self.fields["metric"] = DecimalField(
            decimal_places=1,
            label="Kilograms",
            classes="nhsuk-input--width-4",
            required=True,
            error_messages={
                'required': 'Enter your weight',
                'max_decimal_places': (
                    'Kilograms must be to 1 decimal place, '
                    'for example 90.2kgs'
                ),
            },
            suffix="kg"
        )

    def clean_metric(self):
        return int(self.cleaned_data['metric'] * 10)

    def clean_imperial(self):
        return None

    class Meta:
        model = WeightResponse
        fields = ['metric', 'imperial']
