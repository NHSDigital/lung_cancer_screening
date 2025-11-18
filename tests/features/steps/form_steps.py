from behave import when


@when('I submit my participant id')
def when_I_submit_my_participant_id(context):
    context.page.fill('input[name="participant_id"]', context.participant_id)
    context.page.click('button[type="submit"]')

@when('I fill in and submit my smoking status with "{smoking_status}"')
def when_I_fill_in_and_submit_my_smoking_status(context, smoking_status):
    context.page.get_by_label(smoking_status).check()
    context.page.click("text=Continue")

@when('I fill in and submit my date of birth with "{date_of_birth}"')
def when_I_fill_in_and_submit_my_date_of_birth(context, date_of_birth):
    day, month, year = date_of_birth.split('-')
    context.page.get_by_label('Day').fill(day)
    context.page.get_by_label('Month').fill(month)
    context.page.get_by_label('Year').fill(year)
    context.page.click("text=Continue")

@when(u'I fill in and submit my height with "{height}"')
def when_I_fill_in_and_submit_my_height(context, height):
    context.page.get_by_label('Centimetre').fill(height)
    context.page.click("text=Continue")

@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inch')
@when(u'I fill in and submit my height with "{feet}" feet and "{inches}" inches')
def when_I_fill_in_and_submit_my_height_with_feet_and_inches(context, feet, inches):
    context.page.get_by_label('Feet').fill(feet)
    context.page.get_by_label('Inches').fill(inches)
    context.page.click("text=Continue")

@when(u'I fill in and submit my weight with "{weight}"')
def when_I_fill_in_and_submit_my_weight(context, weight):
    context.page.get_by_label('Kilograms').fill(weight)
    context.page.click("text=Continue")

@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pound')
@when(u'I fill in and submit my weight with "{stone}" stone and "{pounds}" pounds')
def stone_and_pounds(context, stone, pounds):
    context.page.get_by_label('Stone').fill(stone)
    context.page.get_by_label('Pounds').fill(pounds)
    context.page.click("text=Continue")

@when(u'I fill in and submit my respiratory conditions with "{condition_a}" and "{condition_b}"')
def when_I_fill_in_and_submit_my_respiratory_conditions(context, condition_a, condition_b):
    context.page.get_by_label(condition_a).check()
    context.page.get_by_label(condition_b).check()
    context.page.click("text=Continue")

@when('I submit the form')
def when_I_submit_the_form(context):
    context.page.click("text=Continue")
