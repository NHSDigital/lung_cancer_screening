from django import forms

from ...nhsuk_forms.decimal_field import DecimalField
from ..models.response_set import ResponseSet


class MetricWeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert hundreds of grams to kg for display
        if self.instance and self.instance.weight_metric is not None:
            self.initial['weight_metric'] = self.instance.weight_metric / 10

        self.fields["weight_metric"] = DecimalField(
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

    def clean_weight_metric(self):
        return self.cleaned_data['weight_metric'] * 10

    def clean_weight_imperial(self):
        return None

    class Meta:
        model = ResponseSet
        fields = ['weight_metric', 'weight_imperial']
