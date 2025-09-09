from django.test import TestCase
from django.urls import reverse
from datetime import date

from lung_cancer_screening.questions.models.participant import Participant

class TestResponses(TestCase):

    def setUp(self):
        self.participant = Participant.objects.create(unique_id='12345')
        self.response_set = self.participant.responseset_set.create(
            have_you_ever_smoked=True,
            date_of_birth=date(2000, 9, 8)
        )

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:responses"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_participants_responses(self):
        response = self.client.get(reverse("questions:responses"))

        self.assertContains(response, self.response_set.get_have_you_ever_smoked_display())
        self.assertContains(response, self.response_set.date_of_birth)

    def test_get_does_not_contain_responses_for_other_participants(self):
        other_participant = Participant.objects.create(unique_id='67890')
        other_date_response = other_participant.responseset_set.create(have_you_ever_smoked=0, date_of_birth=date(1990, 1, 1))

        response = self.client.get(reverse("questions:responses"))

        self.assertNotContains(
            response, other_date_response.get_have_you_ever_smoked_display())
        self.assertNotContains(response, other_date_response.date_of_birth)

    def test_post_redirects_to_your_results(self):
        response = self.client.post(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:your_results"))

    def test_post_marks_the_result_set_as_submitted(self):
        self.client.post(reverse("questions:responses"))

        self.assertIsNotNone(self.participant.responseset_set.last().submitted_at)
