
from django import forms
from django.forms import widgets

from .choice_field import BoundChoiceField

class TypedChoiceField(forms.TypedChoiceField):
    """
    A TypedChoiceField that renders using NHS.UK design system radios/select
    components.
    """

    widget = widgets.RadioSelect
    bound_field_class = BoundChoiceField

    def __init__(
        self,
        *args,
        hint=None,
        label_classes=None,
        label_is_page_heading=False,
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = TypedChoiceField._template_name(
            kwargs.get("widget", self.widget)
        )

        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes
        self.label_is_page_heading = label_is_page_heading
        super().__init__(*args, **kwargs)

    @staticmethod
    def _template_name(widget):
        return "radios.jinja"
