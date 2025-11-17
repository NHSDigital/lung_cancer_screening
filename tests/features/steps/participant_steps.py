from behave import given
from django.utils import timezone
from lung_cancer_screening.questions.models.participant import Participant


@given('a participant {participant_id} exists')
@given('the participant {participant_id} exists')
def given_a_participant_exists(context, participant_id):
    Participant.objects.create(unique_id=participant_id)


@given('I have already submitted my responses')
def given_I_have_already_submitted_my_responses(context):
    context.participant_id = 'abc123'
    participant = Participant.objects.create(unique_id=context.participant_id)
    participant.responseset_set.create(
        submitted_at=timezone.now()
    )

@given('I have started the questionnaire')
def given_i_have_started_the_questionnaire(context):
    context.participant_id = 'abc123'
    context.page.goto(f'{context.live_server_url}/start')
    context.page.fill('input[name="participant_id"]', context.participant_id)
    context.page.click('button[type="submit"]')
