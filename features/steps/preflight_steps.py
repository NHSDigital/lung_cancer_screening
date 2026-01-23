from behave import given

from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    ResponseSetFactory,
)
from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import (
    HaveYouEverSmokedResponseFactory,
)
from lung_cancer_screening.questions.models.have_you_ever_smoked_response import (
    HaveYouEverSmokedValues,
)


@given('I have answered have you ever smoked with "Yes, I used to smoke"')
def given_i_have_answered_have_your_ever_smoked_with_yes_i_used_to_smoke(context):
    response_set = ResponseSetFactory.create(
        user=context.current_user,
    )
    HaveYouEverSmokedResponseFactory.create(
        response_set=response_set,
        value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY,
    )
