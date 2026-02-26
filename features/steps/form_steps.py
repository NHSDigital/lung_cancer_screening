from behave import when, then
from datetime import datetime
from dateutil.relativedelta import relativedelta

from features.steps.navigation_steps import when_i_click

@when('I check "{value}" and submit')
def when_i_check_value_and_submit(context, value):
    context.page.get_by_label(value, exact=True).check()
    when_i_submit_the_form(context)

@when("I fill in \"{field}\" as \"{value}\" and submit")
def when_i_enter_value_and_submit(context, field, value):
    context.page.get_by_label(field).fill(value)
    when_i_submit_the_form(context)

@when('I fill in and submit my smoking status with "{smoking_status}"')
def when_i_fill_in_and_submit_my_smoking_status(context, smoking_status):
    context.page.get_by_label(smoking_status).check()
    when_i_submit_the_form(context)

@when('I fill in and submit my date of birth with "{date_of_birth}"')
def when_i_fill_in_and_submit_my_date_of_birth(context, date_of_birth):
    day, month, year = date_of_birth.split('-')
    context.page.get_by_label('Day').fill(day)
    context.page.get_by_label('Month').fill(month)
    context.page.get_by_label('Year').fill(year)
    when_i_submit_the_form(context)

@when(u'I fill in and submit my date of birth as {years} years ago')
def when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago(context, years):
    date_of_birth = datetime.now() - relativedelta(years=int(years))
    context.page.get_by_label('Day').fill(str(date_of_birth.day))
    context.page.get_by_label('Month').fill(str(date_of_birth.month))
    context.page.get_by_label('Year').fill(str(date_of_birth.year))
    when_i_submit_the_form(context)

@when(u'I fill in and submit my height with "{height}"')
def when_i_fill_in_and_submit_my_height(context, height):
    context.page.get_by_label('Centimetre').fill(height)
    when_i_submit_the_form(context)

@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inch')
@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inches')
def when_i_fill_in_and_submit_my_height_with_feet_and_inches(context, feet, inches):
    context.page.get_by_label('Feet').fill(feet)
    context.page.get_by_label('Inches').fill(inches)
    when_i_submit_the_form(context)

@when(u'I fill in and submit my weight with "{weight}"')
def when_i_fill_in_and_submit_my_weight(context, weight):
    context.page.get_by_label('Kilograms').fill(weight)
    when_i_submit_the_form(context)

@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pound')
@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pounds')
def stone_and_pounds(context, stone, pounds):
    context.page.get_by_label('Stone').fill(stone)
    context.page.get_by_label('Pounds').fill(pounds)
    when_i_submit_the_form(context)

@when(u'I fill in and submit my sex at birth with "{sex_at_birth}"')
def when_i_fill_in_and_submit_my_sex_at_birth(context, sex_at_birth):
    context.page.get_by_label(sex_at_birth, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my gender with "{gender}"')
def when_i_fill_in_and_submit_my_gender(context, gender):
    context.page.get_by_label(gender, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my ethnicity with "{ethnicity}"')
def when_i_fill_in_and_submit_my_ethnicity(context, ethnicity):
    context.page.get_by_label(ethnicity, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my education with "{education}"')
def when_i_fill_in_and_submit_my_education(context, education):
    context.page.get_by_label(education, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my respiratory conditions with "{condition_a}" and "{condition_b}"')
def when_i_fill_in_and_submit_my_respiratory_conditions(context, condition_a, condition_b):
    context.page.get_by_label(condition_a).check()
    context.page.get_by_label(condition_b).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my asbestos exposure with "{asbestos_exposure}"')
def when_i_fill_in_and_submit_my_asbestos_exposure(context, asbestos_exposure):
    context.page.get_by_label(asbestos_exposure, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my cancer diagnosis with "{cancer_diagnosis}"')
def when_i_fill_in_and_submit_my_cancer_diagnosis(context, cancer_diagnosis):
    context.page.get_by_label(cancer_diagnosis, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my family history lung cancer with "{family_history_lung_cancer}"')
def when_i_fill_in_and_submit_my_cancer_diagnosis(context, family_history_lung_cancer):
    context.page.get_by_label(family_history_lung_cancer, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my relatives age when diagnosed with "{relatives_age_when_diagnosed}"')
def when_i_fill_in_and_submit_my_cancer_diagnosis(context, relatives_age_when_diagnosed):
    context.page.get_by_label(relatives_age_when_diagnosed, exact=True).check()
    when_i_submit_the_form(context)

@when(u'I fill in and submit my periods when you stopped smoking with "{periods_when_you_stopped_smoking}"')
def when_i_fill_in_and_submit_my_periods_when_you_stopped_smoking(context, periods_when_you_stopped_smoking):
    context.page.get_by_label(periods_when_you_stopped_smoking, exact=True).check()
    when_i_submit_the_form(context)

@when('I submit the form')
def when_i_submit_the_form(context):
    when_i_click(context, "Continue")

@then(u'I see "{value}" selected')
def then_i_see_value_selected(context, value):
    assert context.page.get_by_label(value, exact=True).is_checked()

@then(u'I see a date {years} years ago filled in')
def then_i_see_a_date_x_years_ago_filled_in(context, years):
    date_of_birth = datetime.now() - relativedelta(years=int(years))
    assert context.page.get_by_label('Day').input_value() == str(date_of_birth.day)
    assert context.page.get_by_label('Month').input_value() == str(date_of_birth.month)
    assert context.page.get_by_label('Year').input_value() == str(date_of_birth.year)


@then(u'I see "{value}" filled in for "{label}"')
def then_i_see_value_filled_in_for_label(context, value, label):
    assert context.page.get_by_label(label, exact=True).input_value() == value


@when('I check "{label}"')
def when_i_check_label(context, label):
    context.page.get_by_label(label, exact=True).check()


@when('I uncheck "{label}"')
def when_i_uncheck_label(context, label):
    context.page.get_by_label(label, exact=True).uncheck()


@when('I fill in "{label}" with "{value}"')
def when_i_fill_in_label_with_value(context, label, value, exact=True):
    context.page.get_by_label(label, exact=exact).fill(value)
