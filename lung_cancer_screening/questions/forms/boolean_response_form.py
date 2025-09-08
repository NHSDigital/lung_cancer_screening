from django import forms

from lung_cancer_screening.core.form_fields import TypedChoiceField
from ..models.boolean_response import BooleanResponse

class BooleanResponseForm(forms.ModelForm):
    CHOICES = [
        (True, "Yes"),
        (False, "No")
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
            choices=self.CHOICES,
            widget=forms.RadioSelect,
            coerce=lambda x: x == 'True',
            label="Have you ever smoked?",
            label_classes="nhsuk-fieldset__legend--m",
        )

    class Meta:
        model = BooleanResponse
        fields = ['value']
