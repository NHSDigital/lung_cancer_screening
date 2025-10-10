import decimal
from django import forms

from lung_cancer_screening.core.form_fields import DecimalField
from ..models.response_set import ResponseSet

class HeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["height_in_cm"] = DecimalField(
             label="Centimetres",
             classes="nhsuk-input--width-4",
        )



    def clean_height_in_cm(self):
      data = self.cleaned_data['height_in_cm']
      return data*10

    class Meta:
        model = ResponseSet
        fields = ['height']