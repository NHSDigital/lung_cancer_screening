from behave import given

from features.steps.form_steps import (
    when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago,
    when_i_submit_the_form,
    when_i_check_label,
    when_i_fill_in_label_with_value
)

from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    ResponseSetFactory,
)
from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    HaveYouEverSmokedResponseFactory,
)
from lung_cancer_screening.questions.tests.factories.date_of_birth_response_factory import (
    DateOfBirthResponseFactory,
)
from lung_cancer_screening.questions.tests.factories.age_when_started_smoking_response_factory import (
    AgeWhenStartedSmokingResponseFactory,
)


def get_or_create_response_set(context):
    return (
        context.current_user.most_recent_response_set()
        or ResponseSetFactory.create(
            user=context.current_user,
        )
    )


@given('I have answered have you ever smoked with an eligible response')
def given_i_have_answered_have_your_ever_smoked_with_an_eligible_response(context):
    response_set = get_or_create_response_set(context)

    HaveYouEverSmokedResponseFactory.create(
        response_set=response_set,
        eligible=True,
    )

@given('I have answered date of birth with an eligible date of birth')
def given_i_have_answered_date_of_birth_with_an_eligible_date_of_birth(context):
    response_set = get_or_create_response_set(context)

    DateOfBirthResponseFactory.create(
        response_set=response_set,
        eligible=True,
    )


@given("I have answered questions showing I am eligible")
def given_i_have_answered_questions_showing_i_am_eligible(context):
    ResponseSetFactory.create(
        user=context.current_user,
        eligible=True,
    )

@given('I have answered questions showing I have smoked for "{years}" years')
def given_i_have_answered_questions_showing_i_have_smoked_for_years_years(context, years):
    response_set = get_or_create_response_set(context)

    AgeWhenStartedSmokingResponseFactory.create(
        response_set=response_set,
        value=response_set.date_of_birth_response.age_in_years() - int(years),
    )

@given('I have answered questions showing I am aged "{years}" years old')
def given_i_have_answered_questions_showing_i_am_aged_60_years_old(context, years):
    context.page.goto(f"{context.live_server_url}/date-of-birth")
    when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago(context, years)


@given('I have answered questions showing I stopped smoking for "{years}" years')
def given_i_have_answered_questions_showing_i_stopped_smoking_for_years_years(context, years):
    context.page.goto(f"{context.live_server_url}/periods-when-you-stopped-smoking")
    when_i_check_label(context, "Yes")
    when_i_fill_in_label_with_value(context, "Enter the total number of years you stopped smoking for", years)
    when_i_submit_the_form(context)
