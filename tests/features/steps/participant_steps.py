from behave import given
from django.utils import timezone
from lung_cancer_screening.questions.models.participant import Participant


@given('a participant {participant_id} exists')
@given('the participant {participant_id} exists')
def given_a_participant_exists(context, participant_id):
    Participant.objects.create(unique_id=participant_id)


@given('the participant {participant_id} has submitted their responses')
def given_the_participant_has_submitted_their_responses(context, participant_id):
    participant = Participant.objects.get(unique_id=participant_id)
    participant.responseset_set.create(
        submitted_at=timezone.now()
    )
