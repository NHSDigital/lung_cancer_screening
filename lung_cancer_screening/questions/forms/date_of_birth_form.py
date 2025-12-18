from django import forms
from datetime import date

from ..models.response_set import ResponseSet
from ...nhsuk_forms.split_date_field import SplitDateField


class DateOfBirthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        invalid_error_message = 'Date of birth must be a real date'
        self.fields["date_of_birth"] = SplitDateField(
            max_value=date.today(),
            required=True,
            require_all_fields=False,
            label="What is your date of birth?",
            label_is_page_heading=True,
            label_classes="nhsuk-fieldset__legend--l",
            hint="For example, 15 3 1965",
            error_messages={
                'required': 'Enter your date of birth',
                'incomplete': 'Enter your full date of birth',
                'invalid': invalid_error_message,
                'day_bounds': invalid_error_message,
                'month_bounds': invalid_error_message
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['date_of_birth']
