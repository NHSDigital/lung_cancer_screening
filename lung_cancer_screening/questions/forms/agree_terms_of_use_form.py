from django import forms

from ...nhsuk_forms.choice_field import ChoiceField

from ..models.terms_of_use_response import TermsOfUseResponse


class TermsOfUseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"] = ChoiceField(
            choices=[(True, 'I agree')],
            widget=forms.CheckboxInput,
            label="I agree",
            error_messages={
                'required': 'Agree to the terms of use to continue',
                'invalid_choice': 'Agree to the terms of use to continue'
            }
        )
    class Meta:
        model = TermsOfUseResponse
        fields = ['value']
