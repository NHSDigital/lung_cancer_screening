from django.core.exceptions import ValidationError

def validate_singleton_option(value):
    if value and "N" in value and len(value) > 1:
        raise ValidationError(
            "Cannot have singleton value and other values selected",
            code="singleton_option",
        )

