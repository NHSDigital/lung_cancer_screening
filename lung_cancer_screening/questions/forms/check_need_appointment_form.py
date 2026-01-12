from django import forms
from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.check_need_appointment_response import CheckNeedAppointmentResponse


class CheckNeedAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
            choices=[
                (True, 'Yes, one or more of these things applies to me and I need a face-to-face appointment'),
                (False, 'No, I can continue online')
            ],
            widget=forms.RadioSelect,
            label="Do you need to leave the online service and ask for a face-to-face appointment?",
            label_classes="nhsuk-fieldset__legend--m",
            coerce=do_coerce,
            error_messages={
                'required': 'Select if you can continue online'
            }
        )

    class Meta:
        model = CheckNeedAppointmentResponse
        fields = ['value']

def do_coerce(value) :
    return value == "True"
