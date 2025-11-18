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
