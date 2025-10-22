from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from lung_cancer_screening.core.form_fields import BoundChoiceField

class ChoiceField(forms.ChoiceField):
    """
    A ChoiceField that renders using NHS.UK design system radios/select
    components.
    """

    widget = widgets.RadioSelect
    bound_field_class = BoundChoiceField

    def __init__(
        self,
        *args,
        hint=None,
        label_classes=None,
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = ChoiceField._template_name(
            kwargs.get("widget", self.widget)
        )

        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes

        super().__init__(*args, **kwargs)

    @staticmethod
    def _template_name(widget):
        return "forms/radios.jinja"
