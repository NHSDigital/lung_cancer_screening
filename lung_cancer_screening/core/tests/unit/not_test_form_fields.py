import pytest
from django.forms import Form
from django.forms.widgets import (
    CheckboxSelectMultiple,
)
from pytest_django.asserts import assertHTMLEqual

from ..form_fields import (
    CharField,
    MultipleChoiceField,
)
class TestMultipleChoiceField:
    @pytest.fixture
    def form_class(self):
        class TestForm(Form):
            checkbox_field = MultipleChoiceField(
                label="Def",
                label_classes="app-def",
                choices=(("a", "A"), ("b", "B")),
                hint="Pick any number",
                widget=CheckboxSelectMultiple,
            )
            details = CharField(label="Abc", initial="")

        return TestForm

    def test_renders_nhs_checkboxes(self, form_class):
        assertHTMLEqual(
            form_class()["checkbox_field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <fieldset aria-describedby="id_checkbox_field-hint" class="nhsuk-fieldset">
                    <legend class="nhsuk-fieldset__legend app-def">
                        Def
                    </legend>
                    <div class="nhsuk-hint" id="id_checkbox_field-hint">
                        Pick any number
                    </div>
                    <div class="nhsuk-checkboxes" data-module="nhsuk-checkboxes">
                        <div class="nhsuk-checkboxes__item">
                            <input class="nhsuk-checkboxes__input" id="id_checkbox_field" name="checkbox_field" type="checkbox" value="a">
                            <label class="nhsuk-label nhsuk-checkboxes__label" for="id_checkbox_field">A</label>
                        </div>
                        <div class="nhsuk-checkboxes__item">
                            <input class="nhsuk-checkboxes__input" id="id_checkbox_field-2" name="checkbox_field" type="checkbox" value="b">
                            <label class="nhsuk-label nhsuk-checkboxes__label" for="id_checkbox_field-2">B</label>
                        </div>
                    </div>
                </fieldset>
            </div>
            """,
        )

    def test_renders_nhs_checkboxes_with_conditional_html(self, form_class):
        form = form_class()
        form["checkbox_field"].add_conditional_html("b", "<p>Hello</p>")

        assertHTMLEqual(
            form["checkbox_field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <fieldset aria-describedby="id_checkbox_field-hint" class="nhsuk-fieldset">
                    <legend class="nhsuk-fieldset__legend app-def">
                        Def
                    </legend>
                    <div class="nhsuk-hint" id="id_checkbox_field-hint">
                        Pick any number
                    </div>
                    <div class="nhsuk-checkboxes nhsuk-checkboxes--conditional" data-module="nhsuk-checkboxes">
                        <div class="nhsuk-checkboxes__item">
                            <input class="nhsuk-checkboxes__input" id="id_checkbox_field" name="checkbox_field" type="checkbox" value="a">
                            <label class="nhsuk-label nhsuk-checkboxes__label" for="id_checkbox_field">A</label>
                        </div>
                        <div class="nhsuk-checkboxes__item">
                            <input aria-controls="conditional-id_checkbox_field-2" aria-expanded="false" class="nhsuk-checkboxes__input" id="id_checkbox_field-2" name="checkbox_field" type="checkbox" value="b">
                            <label class="nhsuk-label nhsuk-checkboxes__label" for="id_checkbox_field-2">B</label>
                        </div>
                        <div class="nhsuk-checkboxes__conditional nhsuk-checkboxes__conditional--hidden" id="conditional-id_checkbox_field-2">
                            <p>Hello</p>
                        </div>
                    </div>
                </fieldset>
            </div>
            """,
        )
