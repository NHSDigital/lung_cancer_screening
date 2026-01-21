from behave import given
from django.utils import timezone

from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory


@given('I have recently submitted my responses')
def given_i_have_already_submitted_my_responses(context):
    ResponseSetFactory.create(
        user=context.current_user,
        recently_submitted=True
    )

@given('I have started the questionnaire')
def given_i_have_started_the_questionnaire(context):
    context.page.goto(f'{context.live_server_url}/start')
    context.page.click('text=Start')
