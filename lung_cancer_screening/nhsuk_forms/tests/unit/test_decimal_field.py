from django.test import TestCase
from django.forms import Form
from ...decimal_field import DecimalField


class TestDecimalField(TestCase):
    def test_renders_nhs_input(self):
        class TestForm(Form):
            field = DecimalField(label="Abc", initial=1, max_value=10)
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

    def test_renders_nhs_input_with_suffix(self):
        class TestForm(Form):
            field = DecimalField(label="Abc", initial=1, max_value=10, suffix="cm")
        print(TestForm()["field"].as_field_group())
        self.assertHTMLEqual(
            TestForm()["field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <label class="nhsuk-label" for="id_field">
                    Abc
                </label>
                <div class="nhsuk-input__wrapper">
                    <input class="nhsuk-input" id="id_field" name="field" type="number" value="1">
                    <div class="nhsuk-input__suffix" aria-hidden="true">cm</div>
                </div>
            </>
            """,
        )

