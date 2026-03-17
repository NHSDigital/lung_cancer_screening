from django import forms

from ...nhsuk_forms.choice_field import MultipleChoiceField

from ..models.terms_of_use_response import TermsOfUseResponse


class TermsOfUseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"] = MultipleChoiceField(
            choices=[(True, 'I agree')],
            widget=forms.CheckboxSelectMultiple,
            label="Accept terms of use",
            label_classes="nhsuk-u-visually-hidden",
            error_messages={
                "required": "Agree to the terms of use to continue",
                "invalid_choice": "Agree to the terms of use to continue",
                "invalid_list": "Agree to the terms of use to continue"
            }
        )
    class Meta:
        model = TermsOfUseResponse
        fields = ["value"]

    def clean_value(self):
        values = self.cleaned_data.get("value") or []
        return "True" in values
