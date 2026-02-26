from behave import given
from inflection import humanize
from features.steps.debug_steps import screenshot

from features.steps.form_steps import (
    when_i_fill_in_and_submit_my_date_of_birth_as_x_years_ago,
    when_i_submit_the_form,
    when_i_check_label,
    when_i_fill_in_label_with_value
)

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory
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
    when_i_fill_in_label_with_value(context, "Enter the total number of years you stopped smoking", years)
    when_i_submit_the_form(context)


@given('I have answered questions showing I have smoked "{tobacco_types}"')
def given_i_have_answered_questions_showing_i_have_smoked_tobacco_type(
    context, tobacco_types
):
    context.page.goto(f"{context.live_server_url}/types-tobacco-smoking")

    for tobacco_type in tobacco_types.split(","):
        when_i_check_label(context, tobacco_type.strip())

    when_i_submit_the_form(context)


@given('I have answered questions showing I currently smoke "{tobacco_type}"')
def given_i_have_answered_questions_showing_i_currently_smoke_tobacco_type(context, tobacco_type):
    given_i_have_answered_questions_showing_i_have_smoked_tobacco_type(
        context, tobacco_type
    )
    context.page.goto(
        f"{context.live_server_url}/{tobacco_type.lower()}-smoking-current"
    )
    when_i_check_label(context, "Yes")
    when_i_submit_the_form(context)


@given('I have answered questions showing I have smoked "{tobacco_type}" {frequency}')
def given_i_have_answered_questions_showing_i_have_smoked_tobacco_type_frequency(context, tobacco_type, frequency):
    given_i_have_answered_questions_showing_i_have_smoked_tobacco_type(context, tobacco_type)
    context.page.goto(f"{context.live_server_url}/{tobacco_type.lower()}-smoking-frequency")
    when_i_check_label(context, humanize(frequency))
    when_i_submit_the_form(context)

@given('I have answered questions showing I have smoked {amount} "{tobacco_type}" "{frequency}"')
def i_have_answered_questions_showing_i_have_smoked_amount_tobacco_type_frequency(context, amount, tobacco_type, frequency):
    given_i_have_answered_questions_showing_i_have_smoked_tobacco_type_frequency(context, tobacco_type, frequency)
    given_i_have_answered_questions_showing_i_have_smoked_amount_tobacco_type(context, amount, tobacco_type)

@given('I have answered questions showing I have smoked {amount} "{tobacco_type}" as the amount')
def given_i_have_answered_questions_showing_i_have_smoked_amount_tobacco_type(context, amount, tobacco_type):
    context.page.goto(f"{context.live_server_url}/{tobacco_type.lower()}-smoked-amount")
    when_i_fill_in_label_with_value(context, f"Roughly how many {tobacco_type.lower()} do you currently smoke in a normal day?", amount)
    when_i_submit_the_form(context)

@given('I have answered questions showing I have "{level}" my level of "{tobacco_type}" smoking from "{previous_level}"')
def given_i_have_answered_questions_showing_i_have_level_of_smoking(context, level, tobacco_type, previous_level):
    context.page.goto(f"{context.live_server_url}/{tobacco_type.lower()}-smoking-change")
    when_i_check_label(context, f"{TobaccoSmokingHistory.Levels[level.upper()].label} than {previous_level.lower()}")
    when_i_submit_the_form(context)

@given('I have answered questions showing I have "{level}" my frequency of "{tobacco_type}" smoking to "{frequency}"')
def given_i_have_answered_questions_showing_i_have_changed_frequency_of_smoked_tobacco_type(
    context, level, tobacco_type, frequency
):
    given_i_have_answered_questions_showing_i_have_smoked_tobacco_type(
        context, tobacco_type
    )
    context.page.goto(
        f"{context.live_server_url}/{tobacco_type.lower()}-smoking-{level}-frequency"
    )
    when_i_check_label(context, humanize(frequency))
    when_i_submit_the_form(context)

@given('I have answered questions showing I have "{level}" my amount of "{tobacco_type}" smoking to "{amount}"')
def given_i_have_answered_questions_showing_i_have_changed_amount_of_smoked_tobacco_type(context, level, tobacco_type, amount):
    given_i_have_answered_questions_showing_i_have_smoked_tobacco_type(context, tobacco_type)
    context.page.goto(f"{context.live_server_url}/{tobacco_type.lower()}-smoked-{level}-amount")
    screenshot(context)
    when_i_fill_in_label_with_value(context, f"roughly how many {tobacco_type.lower()} did you normally smoke a", amount, exact=False)
    when_i_submit_the_form(context)
