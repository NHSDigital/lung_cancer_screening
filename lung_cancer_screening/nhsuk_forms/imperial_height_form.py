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

        between_feet="Feet must be between 4 and 8"

        feet_kwargs = {
            "min_value": 4,
            "max_value": 8,
            "error_messages": {
                'invalid': 'Feet must be in whole numbers',
                'min_value': between_feet,
                'max_value': between_feet,
                **error_messages,
            },
        }

        between_inches = "Inches must be between 0 and 11"

        inches_kwargs = {
            "min_value": 0,
            "max_value": 11,
            "error_messages": {
                'invalid': 'Inches must be in whole numbers',
                'min_value': between_inches,
                'max_value': between_inches,
                **error_messages,
            },
        }
        fields = (
            IntegerField(**feet_kwargs),
            IntegerField(**inches_kwargs),
        )
        kwargs["template_name"] = "imperial-height-input.jinja"

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
