import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms import Form

from ...split_date_field import SplitDateField

class TestSplitDateField(TestCase):
    def test_clean(self):
        f = SplitDateField(max_value=datetime.date(2026, 6, 30))

        assert f.clean([1, 12, 2025]) == datetime.date(2025, 12, 1)

        with self.assertRaises(ValidationError) as context:
            f.clean(None)

        self.assertEqual(
            context.exception.messages[0],
            "This field is required."
        )

        with self.assertRaises(ValidationError) as context:
            f.clean("")

        self.assertEqual(
            context.exception.messages[0],
            "This field is required."
        )

        with self.assertRaises(ValidationError) as context:
            f.clean("hello")

        self.assertEqual(
            context.exception.messages[0],
            "Enter a valid date."
        )

        with self.assertRaises(ValidationError) as context:
            f.clean(["a", "b", "c"])

        self.assertIn(
            "Enter day as a number.",
            context.exception.messages
        )
        self.assertIn(
            "Enter month as a number.",
            context.exception.messages
        )
        self.assertIn(
            "Enter year as a number.",
            context.exception.messages
        )

        with self.assertRaises(ValidationError) as context:
            f.clean(["", "", ""])

        self.assertEqual(
            context.exception.messages[0],
            "This field is required."
        )

        with self.assertRaises(ValidationError) as context:
            f.clean([0, 13, 1800])

        self.assertIn(
            "Day should be between 1 and 31.",
            context.exception.messages
        )
        self.assertIn(
            "Month should be between 1 and 12.",
            context.exception.messages
        )
        self.assertIn(
            "Year should be between 1900 and 2026.",
            context.exception.messages
        )

        with self.assertRaises(ValidationError) as context:
            f.clean([1, 7, 2026])

        self.assertIn(
            "Enter a date before 30 June 2026.",
            context.exception.messages
        )

    def test_has_changed(self):
        f = SplitDateField(max_value=datetime.date(2026, 12, 31))
        assert f.has_changed([1, 12, 2025], [2, 12, 2025])
        assert f.has_changed([1, 12, 2025], [1, 11, 2025])
        assert f.has_changed([1, 12, 2025], [1, 12, 2026])
        assert not f.has_changed([1, 12, 2025], [1, 12, 2025])

    def test_default_django_render(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 12, 31))

        f = TestForm()

        self.assertHTMLEqual(
            str(f),
            """<div>
            <div class="nhsuk-form-group">
                <fieldset class="nhsuk-fieldset" role="group">
                    <legend class="nhsuk-fieldset__legend nhsuk-fieldset__legend--m">
                        Date
                    </legend>
                    <div class="nhsuk-date-input">
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date">
                                Day
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-2" id="id_date" name="date_0" type="text" inputmode="numeric">
                            </div>
                        </div>
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date_1">
                                Month
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-2" id="id_date_1" name="date_1" type="text" inputmode="numeric">
                            </div>
                        </div>
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date_2">
                                Year
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-4" id="id_date_2" name="date_2" type="text" inputmode="numeric">
                            </div>
                        </div>
                    </div>
                </fieldset>
            </div></div>
            """,
        )

    def test_default_django_render_in_bound_form(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 12, 31))

        f = TestForm({"date_0": "1", "date_1": "12", "date_2": "2025"})

        self.assertHTMLEqual(
            str(f),
            """<div>
            <div class="nhsuk-form-group">
                <fieldset class="nhsuk-fieldset" role="group">
                    <legend class="nhsuk-fieldset__legend nhsuk-fieldset__legend--m">
                        Date
                    </legend>
                    <div class="nhsuk-date-input">
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date">
                                Day
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-2" id="id_date" name="date_0" type="text" inputmode="numeric" value="1">
                            </div>
                        </div>
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date_1">
                                Month
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-2" id="id_date_1" name="date_1" type="text" inputmode="numeric" value="12">
                            </div>
                        </div>
                        <div class="nhsuk-date-input__item">
                            <div class="nhsuk-form-group">
                                <label class="nhsuk-label nhsuk-date-input__label" for="id_date_2">
                                Year
                                </label>
                                <input class="nhsuk-input nhsuk-date-input__input nhsuk-input--width-4" id="id_date_2" name="date_2" type="text" inputmode="numeric" value="2025">
                            </div>
                        </div>
                    </div>
                </fieldset>
            </div></div>
            """,
        )

    def test_form_cleaned_data(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 12, 31))

        f = TestForm({"date_0": "1", "date_1": "12", "date_2": "2025"})

        assert f.is_valid()
        assert f.cleaned_data["date"] == datetime.date(2025, 12, 1)

    def test_bound_field_subwidgets(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 12, 31))

        f = TestForm({"date_0": "1", "date_1": "12", "date_2": "2025"})
        field = f["date"]

        assert len(field.subwidgets) == 3

        assert field.subwidgets[0].data == {
            "attrs": {
                "id": "id_date_0",
                "max": 31,
                "min": 1,
                "required": True,
            },
            "is_hidden": False,
            "name": "date_0",
            "required": False,
            "template_name": "django/forms/widgets/number.html",
            "type": "number",
            "value": "1",
        }

        assert field.subwidgets[1].data == {
            "attrs": {
                "id": "id_date_1",
                "max": 12,
                "min": 1,
                "required": True,
            },
            "is_hidden": False,
            "name": "date_1",
            "required": False,
            "template_name": "django/forms/widgets/number.html",
            "type": "number",
            "value": "12",
        }

        assert field.subwidgets[2].data == {
            "attrs": {
                "id": "id_date_2",
                "max": 2026,
                "min": 1900,
                "required": True,
            },
            "is_hidden": False,
            "name": "date_2",
            "required": False,
            "template_name": "django/forms/widgets/number.html",
            "type": "number",
            "value": "2025",
        }

    def test_subfield_errors_on_form(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 12, 31))

        f = TestForm({"date_0": "1", "date_1": "12", "date_2": "2027"})
        assert not f.is_valid()
        assert f.errors == {"date": ["Year should be between 1900 and 2026."]}

    def test_same_year_but_past_max_value(self):
        class TestForm(Form):
            date = SplitDateField(max_value=datetime.date(2026, 7, 1))

        f = TestForm({"date_0": "1", "date_1": "8", "date_2": "2026"})
        assert not f.is_valid()
        assert f.errors == {"date": ["Enter a date before 1 July 2026."]}
