from django import forms

from ...nhsuk_forms.decimal_field import DecimalField
from ..models.height_response import HeightResponse


class MetricHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert mm to cm for display
        if self.instance and self.instance.metric is not None:
            self.initial['metric'] = self.instance.metric / 10

        self.fields["metric"] = DecimalField(
            decimal_places=1,
            label="Centimetres",
            classes="nhsuk-input--width-4",
            error_messages={
                'required': 'Enter your height',
                "max_decimal_places": (
                    "Centimetres must be to 1 decimal place, "
                    "for example 185.5cm"
                ),
            },
            suffix="cm"
        )

    def clean_metric(self):
        return int(self.cleaned_data['metric'] * 10)

    def clean_imperial(self):
        return None

    class Meta:
        model = HeightResponse
        fields = ['metric', 'imperial']
