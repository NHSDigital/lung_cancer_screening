from django import forms

from ...nhsuk_forms.decimal_field import DecimalField
from ..models.response_set import ResponseSet


class MetricHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert mm to cm for display
        if self.instance and self.instance.height_metric is not None:
            self.initial['height_metric'] = self.instance.height_metric / 10

        self.fields["height_metric"] = DecimalField(
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

    def clean_height_metric(self):
        return self.cleaned_data['height_metric'] * 10

    def clean_height_imperial(self):
        return None

    class Meta:
        model = ResponseSet
        fields = ['height_metric', 'height_imperial']
