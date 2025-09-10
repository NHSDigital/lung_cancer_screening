from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lung_cancer_screening.questions.models.participant import Participant

class TestPostAgeRangeExit(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_redirects_if_the_particpant_has_no_unsubmitted_response_set(self):
        self.participant.responseset_set.all().update(submitted_at=timezone.now())

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:age_range_exit"))

        self.assertEqual(response.status_code, 200)
