from django.test import TestCase
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.date_response import DateResponse

class TestPostDateOfBirth(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="12345")
        self.valid_age = date.today() - relativedelta(years=55)
        self.valid_params = {
            "value_0": self.valid_age.day,
            "value_1": self.valid_age.month,
            "value_2": self.valid_age.year
        }

        self.invalid_age = date.today() - relativedelta(years=20)
        self.invalid_params = {
            "value_0": self.invalid_age.day,
            "value_1": self.invalid_age.month,
            "value_2": self.invalid_age.year
        }

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertEqual(response.status_code, 200)

    def test_post_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_date_response_for_the_participant(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        date_response = DateResponse.objects.first()
        self.assertEqual(date_response.value, self.valid_age)
        self.assertEqual(date_response.participant, self.participant)
        self.assertEqual(date_response.question, "What is your date of birth?")

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_responses_path(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {"value_0": "80000", "value_1": "90000", "value_2": "20000000"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_create_a_date_response_if_the_user_is_not_in_the_correct_age_range(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.invalid_params
        )

        self.assertEqual(DateResponse.objects.count(), 0)

    def test_post_redirects_if_the_user_is_not_in_the_correct_age_range(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.invalid_params
        )

        self.assertRedirects(response, reverse("questions:age_range_exit"))
