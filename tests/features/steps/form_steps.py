from behave import when
from datetime import datetime
from dateutil.relativedelta import relativedelta


@when('I submit my participant id')
def when_i_submit_my_participant_id(context):
    if not hasattr(context, 'participant_id'):
        context.participant_id = 'abc123'
    context.page.fill('input[name="participant_id"]', context.participant_id)
    context.page.click('button[type="submit"]')

@when('I fill in and submit my smoking status with "{smoking_status}"')
def when_i_fill_in_and_submit_my_smoking_status(context, smoking_status):
    context.page.get_by_label(smoking_status).check()
    context.page.click("text=Continue")

@when('I fill in and submit my date of birth with "{date_of_birth}"')
def when_i_fill_in_and_submit_my_date_of_birth(context, date_of_birth):
    day, month, year = date_of_birth.split('-')
    context.page.get_by_label('Day').fill(day)
    context.page.get_by_label('Month').fill(month)
    context.page.get_by_label('Year').fill(year)
    context.page.click("text=Continue")

@when(u'I fill in and submit my date of birth as {years} years ago')
def when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago(context, years):
    date_of_birth = datetime.now() - relativedelta(years=int(years))
    context.page.get_by_label('Day').fill(str(date_of_birth.day))
    context.page.get_by_label('Month').fill(str(date_of_birth.month))
    context.page.get_by_label('Year').fill(str(date_of_birth.year))
    context.page.click("text=Continue")

@when(u'I fill in and submit my height with "{height}"')
def when_i_fill_in_and_submit_my_height(context, height):
    context.page.get_by_label('Centimetre').fill(height)
    context.page.click("text=Continue")

@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inch')
@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inches')
def when_i_fill_in_and_submit_my_height_with_feet_and_inches(context, feet, inches):
    context.page.get_by_label('Feet').fill(feet)
    context.page.get_by_label('Inches').fill(inches)
    context.page.click("text=Continue")

@when(u'I fill in and submit my weight with "{weight}"')
def when_i_fill_in_and_submit_my_weight(context, weight):
    context.page.get_by_label('Kilograms').fill(weight)
    context.page.click("text=Continue")

@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pound')
@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pounds')
def stone_and_pounds(context, stone, pounds):
    context.page.get_by_label('Stone').fill(stone)
    context.page.get_by_label('Pounds').fill(pounds)
    context.page.click("text=Continue")

@when(u'I fill in and submit my sex at birth with "{sex_at_birth}"')
def when_i_fill_in_and_submit_my_sex_at_birth(context, sex_at_birth):
    context.page.get_by_label(sex_at_birth, exact=True).check()
    context.page.click("text=Continue")

@when(u'I fill in and submit my gender with "{gender}"')
def when_i_fill_in_and_submit_my_gender(context, gender):
    context.page.get_by_label(gender, exact=True).check()
    context.page.click("text=Continue")

@when(u'I fill in and submit my ethnicity with "{ethnicity}"')
def when_i_fill_in_and_submit_my_ethnicity(context, ethnicity):
    context.page.get_by_label(ethnicity, exact=True).check()
    context.page.click("text=Continue")

@when(u'I fill in and submit my respiratory conditions with "{condition_a}" and "{condition_b}"')
def when_i_fill_in_and_submit_my_respiratory_conditions(context, condition_a, condition_b):
    context.page.get_by_label(condition_a).check()
    context.page.get_by_label(condition_b).check()
    context.page.click("text=Continue")

@when(u'I fill in and submit my asbestos exposure with "{asbestos_exposure}"')
def when_i_fill_in_and_submit_my_asbestos_exposure(context, asbestos_exposure):
    context.page.get_by_label(asbestos_exposure, exact=True).check()
    context.page.click("text=Continue")

@when('I submit the form')
def when_i_submit_the_form(context):
    context.page.click("text=Continue")
