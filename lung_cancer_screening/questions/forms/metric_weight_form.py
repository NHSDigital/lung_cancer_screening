from django import forms

from lung_cancer_screening.core.form_fields import DecimalField
from ..models.response_set import ResponseSet

class MetricWeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["weight_metric"] = DecimalField(
            label="Kilograms",
            classes="nhsuk-input--width-4",
            required=True,
            error_messages={
                'required': 'Enter your weight.',
            }
        )
    def clean_weight_metric(self):
        return self.cleaned_data['weight_metric'] * 10

    class Meta:
        model = ResponseSet
        fields = ['weight_metric']
