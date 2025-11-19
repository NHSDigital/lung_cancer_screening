from django.test import TestCase
from django.forms import Form

from ...choice_field import ChoiceField, MultipleChoiceField

class TestForm(Form):
    field = ChoiceField(
        label="Abc",
        label_classes="app-abc",
        choices=(("a", "A"), ("b", "B")),
        hint="Pick either one",
    )

class TestMultipleChoiceForm(Form):
    field = MultipleChoiceField(
        label="Select options",
        choices=(("a", "Option A"), ("b", "Option B"), ("c", "Option C")),
        hint="Select all that apply",
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

    def test_renders_labels_as_headers_when_true(self):
        class TestForm(Form):
            field = ChoiceField(
                label="Abc",
                label_classes="app-abc",
                label_is_page_heading=True,
                choices=(("a", "A"), ("b", "B")),
                hint="Pick either one",
            )

        self.assertHTMLEqual(
            TestForm()["field"].as_field_group(),
            """
            <div class="nhsuk-form-group">
                <fieldset aria-describedby="id_field-hint" class="nhsuk-fieldset">
                    <legend class="nhsuk-fieldset__legend app-abc">
                        <h1 class="nhsuk-fieldset__heading">Abc</h1>
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

    def test_checkbox_field_with_choice_hints(self):
        """Test that choice hints are rendered correctly for checkbox fields"""
        form = TestMultipleChoiceForm()
        bound_field = form["field"]

        # Add hints for specific choices
        bound_field.add_hint_for_choice("a", "This is hint for option A")
        bound_field.add_hint_for_choice("b", "This is hint for option B")

        rendered_html = bound_field.as_field_group()

        # Verify the hints are rendered
        self.assertIn('This is hint for option A', rendered_html)
        self.assertIn('This is hint for option B', rendered_html)
        self.assertIn('aria-describedby="id_field_0-item-hint"', rendered_html)
        self.assertIn('aria-describedby="id_field_1-item-hint"', rendered_html)

    def test_get_hint_for_choice_returns_correct_hint(self):
        """Test that get_hint_for_choice returns the correct hint text"""
        form = TestMultipleChoiceForm()
        bound_field = form["field"]

        # Add a hint
        bound_field.add_hint_for_choice("a", "Hint for A")

        # Verify the hint can be retrieved
        self.assertEqual(bound_field.get_hint_for_choice("a"), "Hint for A")

    def test_get_hint_for_choice_returns_none_when_no_hint(self):
        """Test that get_hint_for_choice returns None when no hint is set"""
        form = TestMultipleChoiceForm()
        bound_field = form["field"]

        # No hint added, should return None
        self.assertIsNone(bound_field.get_hint_for_choice("a"))

    def test_checkbox_field_renders_without_hints_when_none_added(self):
        """Test that checkbox field renders correctly when no hints are added"""
        form = TestMultipleChoiceForm()
        rendered_html = form["field"].as_field_group()

        # Should render without hint elements
        self.assertNotIn('nhsuk-checkboxes__hint', rendered_html)

    def test_radio_field_with_choice_hints(self):
        """Test that choice hints are rendered correctly for radio fields"""
        form = TestForm()
        bound_field = form["field"]

        # Add hints for specific choices
        bound_field.add_hint_for_choice("a", "This is hint for option A")
        bound_field.add_hint_for_choice("b", "This is hint for option B")

        rendered_html = bound_field.as_field_group()

        # Verify the hints are rendered
        self.assertIn('This is hint for option A', rendered_html)
        self.assertIn('This is hint for option B', rendered_html)
        self.assertIn('aria-describedby="id_field-item-hint"', rendered_html)
        self.assertIn('aria-describedby="id_field-2-item-hint"', rendered_html)

    def test_radio_field_renders_without_hints_when_none_added(self):
        """Test that radio field renders correctly when no hints are added"""
        form = TestForm()
        rendered_html = form["field"].as_field_group()

        # Should render without hint elements for individual items
        self.assertNotIn('nhsuk-radios__hint', rendered_html)
