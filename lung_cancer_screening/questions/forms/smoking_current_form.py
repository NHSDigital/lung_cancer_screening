from django import forms

from ..models import SmokingCurrentResponse

from ...nhsuk_forms.typed_choice_field import TypedChoiceField

class SmokingCurrentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect,
        label="Do you currently smoke cigarettes?",
        label_classes="nhsuk-fieldset__legend--l",
        label_is_page_heading=True,
        coerce=lambda x: x == 'True',
        error_messages={
            'required': 'Select if you currently smoke cigarettes',
        }
    )

    class Meta:
        model = SmokingCurrentResponse
        fields = ['value']
