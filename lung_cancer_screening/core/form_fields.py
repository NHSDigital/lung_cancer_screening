from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from lung_cancer_screening.nhsuk_forms.utils.date_formatting import format_date
from lung_cancer_screening.nhsuk_forms.integer_field import IntegerField

class DecimalField(forms.DecimalField):
    def __init__(
        self,
        *args,
        hint=None,
        label_classes=None,
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = "forms/input.jinja"

        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes

        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)

        # Don't use min/max/step attributes.
        attrs.pop("min", None)
        attrs.pop("max", None)
        attrs.pop("step", None)

        return attrs


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
        if (isinstance(widget, type) and widget is widgets.RadioSelect) or isinstance(
            widget, widgets.RadioSelect
        ):
            return "forms/radios.jinja"
        elif (isinstance(widget, type) and widget is widgets.Select) or isinstance(
            widget, widgets.Select
        ):
            return "forms/select.jinja"


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
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = TypedChoiceField._template_name(
            kwargs.get("widget", self.widget)
        )

        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes

        super().__init__(*args, **kwargs)

    @staticmethod
    def _template_name(widget):
        if (isinstance(widget, type) and widget is widgets.RadioSelect) or isinstance(
            widget, widgets.RadioSelect
        ):
            return "forms/radios.jinja"
        elif (isinstance(widget, type) and widget is widgets.Select) or isinstance(
            widget, widgets.Select
        ):
            return "forms/select.jinja"



class MultipleChoiceField(forms.MultipleChoiceField):
    """
    A MultipleChoiceField that renders using the NHS.UK design system checkboxes
    component.
    """

    widget = widgets.CheckboxSelectMultiple
    bound_field_class = BoundChoiceField

    def __init__(
        self,
        *args,
        hint=None,
        label_classes=None,
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = "forms/checkboxes.jinja"

        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes

        super().__init__(*args, **kwargs)


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


class ImperialWeightWidget(widgets.MultiWidget):
    """
    A widget that splits weight into stone and pounds inputs.
    """

    def __init__(self, attrs=None):
        weight_widgets = (
            widgets.NumberInput(attrs=attrs),
            widgets.NumberInput(attrs=attrs),
        )
        super().__init__(weight_widgets, attrs)

    def decompress(self, value):
        """
        Convert total pounds back to stone and pounds for display.
        """
        if value:
            stone = int(value // 14)
            pounds = value % 14
            return [stone, pounds]
        return [None, None]

    def subwidgets(self, name, value, attrs=None):
        """
        Expose data for each subwidget, so that we can render them separately in the template.
        """
        context = self.get_context(name, value, attrs)
        for subwidget in context["widget"]["subwidgets"]:
            yield subwidget


class ImperialWeightField(forms.MultiValueField):
    """
    A field that combines stone and pounds into a single weight value in total pounds.
    """

    widget = ImperialWeightWidget

    def __init__(self, *args, **kwargs):
        error_messages = kwargs.get("error_messages", {})

        stone_kwargs = {
            "min_value": 0,
            "max_value": 50,
            "error_messages": {
                'invalid': 'Stone must be in whole numbers.',
                'min_value': 'Weight must be between 4 stone and 50 stone.',
                'max_value': 'Weight must be between 4 stone and 50 stone.',
                **error_messages,
            },
        }
        pounds_kwargs = {
            "min_value": 0,
            "max_value": 13,
            "error_messages": {
                'invalid': 'Pounds must be in whole numbers.',
                'min_value': 'Pounds must be between 0 and 13.',
                'max_value': 'Pounds must be between 0 and 13.',
                **error_messages,
            },
        }
        fields = (
            IntegerField(**stone_kwargs),
            IntegerField(**pounds_kwargs),
        )
        kwargs["template_name"] = "forms/imperial-weight-input.jinja"

        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Convert stone and pounds to total pounds.
        """
        if data_list and all(item is not None for item in data_list):
            stone, pounds = data_list
            total_pounds = stone * 14 + pounds
            return int(total_pounds)
        return None
