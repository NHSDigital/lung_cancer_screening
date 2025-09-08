from django import forms
from datetime import date

from ..models.response_set import ResponseSet
from lung_cancer_screening.core.form_fields import SplitDateField

class DateOfBirthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["date_of_birth"] = SplitDateField(
            max_value=date.today(),
            required=False,
            hint="For example, 15 3 2025",
            label="What is your date of birth?"
        )

    class Meta:
        model = ResponseSet
        fields = ['date_of_birth']
