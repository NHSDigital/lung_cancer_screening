from django import forms
from django.forms import widgets

from lung_cancer_screening.nhsuk_forms.integer_field import IntegerField


class ImperialHeightWidget(widgets.MultiWidget):
    """
    A widget that splits height into feet and inches inputs.
    """

    def __init__(self, attrs=None):
        height_widgets = (
            widgets.NumberInput(attrs=attrs),
            widgets.NumberInput(attrs=attrs),
        )
        super().__init__(height_widgets, attrs)

    def decompress(self, value):
        """
        Convert total inches back to feet and inches for display.
        """
        if value:
            feet = int(value // 12)
            inches = value % 12
            return [feet, inches]
        return [None, None]

    def subwidgets(self, name, value, attrs=None):
        """
        Expose data for each subwidget, so that we can render them separately in the template.
        """
        context = self.get_context(name, value, attrs)
        for subwidget in context["widget"]["subwidgets"]:
            yield subwidget


class ImperialHeightField(forms.MultiValueField):
    """
    A field that combines feet and inches into a single height value in cm.
    """

    widget = ImperialHeightWidget

    def __init__(self, *args, **kwargs):
        error_messages = kwargs.get("error_messages", {})

        feet_kwargs = {
            "error_messages": {
                'invalid': 'Feet must be in whole numbers.',
                **error_messages,
            },
        }
        inches_kwargs = {
            "error_messages": {
                'invalid': 'Inches must be in whole numbers.',
                **error_messages,
            },
        }
        fields = (
            IntegerField(**feet_kwargs),
            IntegerField(**inches_kwargs),
        )
        kwargs["template_name"] = "forms/imperial-height-input.jinja"

        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Convert feet and inches to total inches.
        """
        if data_list and all(data_list):
            feet, inches = data_list
            total_inches = feet * 12 + inches
            return int(total_inches)
        return None
