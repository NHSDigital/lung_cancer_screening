import decimal
from django import forms

from lung_cancer_screening.core.form_fields import DecimalField
from ..models.response_set import ResponseSet

class MetricHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["height_feet"] = DecimalField(
             label="Feet",
             classes="nhsuk-input--width-4",
        )
        
        self.fields["height_inches"] = DecimalField(
             label="Inches",
             classes="nhsuk-input--width-4",
        )

    def clean_height(self):
      data = self.cleaned_data['height_feet']*12 + self.cleaned_data['height_inches']
      return data*2.54

    class Meta:
        model = ResponseSet
        fields = ['height']