from django import forms

from ..models import SmokingCurrentResponse

from ...nhsuk_forms.typed_choice_field import TypedChoiceField

class SmokingCurrentForm(forms.ModelForm):
    def __init__(self, tobacco_smoking_history, *args, **kwargs):
        self.tobacco_smoking_history = tobacco_smoking_history
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect,
        label=self.label(),
        label_classes="nhsuk-fieldset__legend--l",
        label_is_page_heading=True,
        coerce=lambda x: x == 'True',
        error_messages={
            'required': self.required_error_message(),
        }
    )


    def label(self):
        return f"Do you currently smoke {self.tobacco_smoking_history.human_type().lower()}?"


    def required_error_message(self):
        return f"Select if you currently smoke {self.tobacco_smoking_history.human_type().lower()}"


    class Meta:
        model = SmokingCurrentResponse
        fields = ['value']
