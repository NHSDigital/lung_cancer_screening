from behave import given
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    ResponseSetFactory,
)
from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    HaveYouEverSmokedResponseFactory,
)
from lung_cancer_screening.questions.models.have_you_ever_smoked_response import (
    HaveYouEverSmokedValues,
)
from lung_cancer_screening.questions.tests.factories.date_of_birth_response_factory import (
    DateOfBirthResponseFactory,
)
from lung_cancer_screening.questions.tests.factories.check_need_appointment_response_factory import (
    CheckNeedAppointmentResponseFactory,
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
def step_impl(context):
    ResponseSetFactory.create(
        user=context.current_user,
        eligible=True,
    )

