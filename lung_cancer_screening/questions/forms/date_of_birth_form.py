from django import forms
from datetime import date

from ..models.response_set import ResponseSet
from lung_cancer_screening.core.form_fields import SplitDateField

class DateOfBirthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["date_of_birth"] = SplitDateField(
            max_value=date.today(),
            required=True,
            require_all_fields=False,
            label="What is your date of birth?",
            hint="For example, 15 3 1965",
            error_messages={
                'required': 'Enter your date of birth.',
                'incomplete': 'Enter your full date of birth.',
                'invalid': 'Date of birth must be a real date.'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['date_of_birth']
