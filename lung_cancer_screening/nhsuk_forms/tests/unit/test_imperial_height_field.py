from django.test import TestCase
from django.forms import Form
from ...imperial_height_field import ImperialHeightField


class TestImperialHeightField(TestCase):
    def test_renders_nhs_input(self):
        class TestForm(Form):
            field = ImperialHeightField(label="Abc")

        self.assertHTMLEqual(
            TestForm()["field"].as_field_group(),
            """
            <div id="field" class="multi-field-input nhsuk-form-group">
                <div class="multi-field-input__item">
                    <div class="nhsuk-form-group">
                        <label class="nhsuk-label" for="id_field_0">
                            Feet
                        </label>
                        <div class="nhsuk-input__wrapper">
                            <input class="nhsuk-input nhsuk-input--width-4" id="id_field_0" name="field_0" type="number">
                            <div class="nhsuk-input__suffix" aria-hidden="true">ft</div>
                        </div>
                    </div>
                </div>

                <div class="multi-field-input__item">
                    <div class="nhsuk-form-group">
                        <label class="nhsuk-label" for="id_field_1">
                            Inches
                        </label>
                        <div class="nhsuk-input__wrapper">
                            <input class="nhsuk-input nhsuk-input--width-4" id="id_field_1" name="field_1" type="number">
                            <div class="nhsuk-input__suffix" aria-hidden="true">in</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
        )
