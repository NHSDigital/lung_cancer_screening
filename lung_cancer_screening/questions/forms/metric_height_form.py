from django import forms

from lung_cancer_screening.core.form_fields import DecimalField
from ..models.response_set import ResponseSet

class MetricHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["height"] = DecimalField(
            label="Centimetres",
            classes="nhsuk-input--width-4",
            error_messages={
                'required': 'Enter your height.',
            }
        )

    def clean_height(self):
        return self.cleaned_data['height'] * 10

    def clean_height_imperial(self):
        return None

    class Meta:
        model = ResponseSet
        fields = ['height', 'height_imperial']
