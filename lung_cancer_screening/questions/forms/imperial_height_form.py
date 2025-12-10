from django import forms

from ...nhsuk_forms.imperial_height_field import ImperialHeightField
from ..models.response_set import ResponseSet

class ImperialHeightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.instance.user = self.user

        self.fields["height_imperial"] = ImperialHeightField(
            label="Height",
            required=True,
            require_all_fields=False,
            error_messages={
                'required': 'Enter your height',
            }
        )

    def clean_height(self):
        return None

    class Meta:
        model = ResponseSet
        fields = ['height_imperial', 'height']
