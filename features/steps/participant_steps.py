from behave import given
from django.utils import timezone


@given('I have already submitted my responses')
def given_i_have_already_submitted_my_responses(context):
    context.current_user.responseset_set.create(
        submitted_at=timezone.now()
    )

@given('I have started the questionnaire')
def given_i_have_started_the_questionnaire(context):
    context.page.goto(f'{context.live_server_url}/start')
    context.page.click('text=Start')
