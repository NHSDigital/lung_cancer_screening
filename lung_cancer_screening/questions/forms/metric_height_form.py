import decimal
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
        )

    def clean_height(self):
      data = self.cleaned_data['height']
      return data*10

    class Meta:
        model = ResponseSet
        fields = ['height']