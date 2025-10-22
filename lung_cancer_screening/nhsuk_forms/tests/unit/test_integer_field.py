from django.test import TestCase
from django.forms import Form
from ...integer_field import IntegerField


class TestForm(Form):
    field = IntegerField(label="Abc", initial=1, max_value=10)

class TestIntegerField(TestCase):
    def test_renders_nhs_input(self):
        self.assertHTMLEqual(
            TestForm()["field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <label class="nhsuk-label" for="id_field">
                    Abc
                </label><input class="nhsuk-input" id="id_field" name="field" type="number" value="1">
            </div>
            """,
        )

