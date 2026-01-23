from behave import given
from django.utils import timezone

from features.steps.form_steps import when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago
from features.steps.navigation_steps import given_i_go_to
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

@given("I am {years:d} years old")
def given_i_am_years_old(context, years):
    given_i_go_to(context, '/date-of-birth')
    when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago(context, years)
