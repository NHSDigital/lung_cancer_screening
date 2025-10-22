from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _


class BoundChoiceField(forms.BoundField):
    """
    Specialisation of BoundField that can deal with conditionally shown fields,
    and divider content between choices.
    This can be used to render a set of radios or checkboxes with text boxes to capture
    more details.
    """

    def __init__(self, form: forms.Form, field: "ChoiceField", name: str):
        super().__init__(form, field, name)

        self._conditional_html = {}
        self.dividers = {}

    def add_conditional_html(self, value, html):
        if isinstance(self.field.widget, widgets.Select):
            raise ValueError(
                "select component does not support conditional fields")

        self._conditional_html[value] = html

    def conditional_html(self, value):
        return self._conditional_html.get(value)

    def add_divider_after(self, previous, divider):
        self.dividers[previous] = divider

    def get_divider_after(self, previous):
        return self.dividers.get(previous)
