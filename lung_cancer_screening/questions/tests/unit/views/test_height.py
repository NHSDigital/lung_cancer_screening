from django.test import TestCase
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from ....models.participant import Participant


class TestPostDateOfBirth(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()

        self.valid_height = 170
        self.valid_params = {"height": self.valid_height}
        self.invalid_height = 80000

        session = self.client.session
        session['participant_id'] = self.participant.unique_id

        session.save()

    def test_get_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existent participant"
        session.save()

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:height"))

        self.assertEqual(response.status_code, 200)

    def test_post_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existent participant"
        session.save()

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_set_for_the_participant(self):
        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()

        self.assertEqual(response_set.height, self.valid_height*10)
        self.assertEqual(response_set.participant, self.participant)

    def test_post_redirects_to_responses_path(self):
        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:height"),
            {"height": "a"}
        )

        self.assertEqual(response.status_code, 422)


# If nothing is entered - Enter your height
# User enters a height that is outside the accepted range (cms) - Height must be between 139.7cm and 243.8 cm
# User enters a height that is outside the accepted range (feet and inches) - Height must be between 4 feet 7 inches and 8 feet
# User enters a reading for feet that is outside the accepted range - Feet must be between 4 and 8
# User enters a reading for inches that is outside the accepted range - Inches must be between 0 and 11
# User enters a reading for feet using a decimal point - Feet must be in whole numbers
# User enters a reading for inches using a decimal point - I