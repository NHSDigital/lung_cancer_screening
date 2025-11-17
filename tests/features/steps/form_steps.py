from behave import when


@when('the participant {participant_id} submits their participant id')
def when_the_participant_submits_their_participant_id(context, participant_id):
    context.page.fill('input[name="participant_id"]', participant_id)
    context.page.click('button[type="submit"]')
