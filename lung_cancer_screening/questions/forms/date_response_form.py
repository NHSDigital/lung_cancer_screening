from django import forms
from datetime import date

from ..models.date_response import DateResponse
from lung_cancer_screening.core.form_fields import SplitDateField

class DateResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = SplitDateField(
            max_value=date.today(),
            required=False,
            hint="For example, 15 3 2025",
            label="What is your date of birth?"
        )

    class Meta:
        model = DateResponse
        fields = ['value']
