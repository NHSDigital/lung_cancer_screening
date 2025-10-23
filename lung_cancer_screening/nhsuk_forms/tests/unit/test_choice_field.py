from django.test import TestCase
from django.forms import Form

from ...choice_field import ChoiceField

class TestForm(Form):
    field = ChoiceField(
        label="Abc",
        label_classes="app-abc",
        choices=(("a", "A"), ("b", "B")),
        hint="Pick either one",
    )

class TestChoiceField(TestCase):
    def test_renders_nhs_radios(self):
        self.assertHTMLEqual(
            TestForm()["field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <fieldset aria-describedby="id_field-hint" class="nhsuk-fieldset">
                    <legend class="nhsuk-fieldset__legend app-abc">
                        Abc
                    </legend>
                    <div class="nhsuk-hint" id="id_field-hint">
                        Pick either one
                    </div>
                    <div class="nhsuk-radios" data-module="nhsuk-radios">
                        <div class="nhsuk-radios__item">
                            <input class="nhsuk-radios__input" id="id_field" name="field" type="radio" value="a">
                            <label class="nhsuk-label nhsuk-radios__label" for="id_field">A</label>
                        </div>
                        <div class="nhsuk-radios__item">
                            <input class="nhsuk-radios__input" id="id_field-2" name="field" type="radio" value="b">
                            <label class="nhsuk-label nhsuk-radios__label" for="id_field-2">B</label>
                        </div>
                    </div>
                </fieldset>
            </div>
            """,
        )

    def test_renders_radios_with_conditional_html(self):
        form = TestForm()
        form["field"].add_conditional_html("b", "<p>Hello</p>")

        self.assertHTMLEqual(
            form["field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <fieldset aria-describedby="id_field-hint" class="nhsuk-fieldset">
                    <legend class="nhsuk-fieldset__legend app-abc">
                        Abc
                    </legend>
                    <div class="nhsuk-hint" id="id_field-hint">
                        Pick either one
                    </div>
                    <div class="nhsuk-radios nhsuk-radios--conditional" data-module="nhsuk-radios">
                        <div class="nhsuk-radios__item">
                            <input class="nhsuk-radios__input" id="id_field" name="field" type="radio" value="a">
                            <label class="nhsuk-label nhsuk-radios__label" for="id_field">A</label>
                        </div>
                        <div class="nhsuk-radios__item">
                            <input aria-controls="conditional-id_field-2" aria-expanded="false" class="nhsuk-radios__input" id="id_field-2" name="field" type="radio" value="b">
                            <label class="nhsuk-label nhsuk-radios__label" for="id_field-2">B</label>
                        </div>
                        <div class="nhsuk-radios__conditional nhsuk-radios__conditional--hidden" id="conditional-id_field-2">
                            <p>Hello</p>
                        </div>
                    </div>
                </fieldset>
            </div>
            """,
        )

    def test_adding_dividers_via_boundfield(self):
        bound_field = TestForm()["field"]
        bound_field.add_divider_after("a", "or")
        assert bound_field.get_divider_after("a") == "or"
