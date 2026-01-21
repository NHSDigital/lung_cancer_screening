from django import forms


class IntegerField(forms.IntegerField):
    def __init__(
        self,
        *args,
        hint=None,
        label_classes=None,
        label_is_page_heading=False,
        classes=None,
        **kwargs,
    ):
        kwargs["template_name"] = "input.jinja"

        self.suffix = kwargs.pop("suffix", None)
        self.prefix = kwargs.pop("prefix", None)
        self.hint = hint
        self.classes = classes
        self.label_classes = label_classes
        self.label_is_page_heading = label_is_page_heading

        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)

        # Don't use min/max/step attributes.
        attrs.pop("min", None)
        attrs.pop("max", None)
        attrs.pop("step", None)

        return attrs
