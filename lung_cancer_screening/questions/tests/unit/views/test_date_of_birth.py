from django.test import TestCase
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .helpers.authentication import login_user
from ....models.participant import Participant

class TestPostDateOfBirth(TestCase):
    def setUp(self):
        login_user(self.client)

        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()
        self.valid_age = date.today() - relativedelta(years=55)
        self.valid_params = {
            "date_of_birth_0": self.valid_age.day,
            "date_of_birth_1": self.valid_age.month,
            "date_of_birth_2": self.valid_age.year
        }

        self.invalid_age = date.today() - relativedelta(years=20)
        self.invalid_params = {
            "date_of_birth_0": self.invalid_age.day,
            "date_of_birth_1": self.invalid_age.month,
            "date_of_birth_2": self.invalid_age.year
        }

        session = self.client.session
        session['participant_id'] = self.participant.unique_id
        session.save()

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        participant = Participant.objects.create(unique_id="abcdef")
        self.client.logout()
        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/date-of-birth", fetch_redirect_response=False)

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

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()
        participant = Participant.objects.create(unique_id="abcdef")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/date-of-birth", fetch_redirect_response=False)

    def test_post_redirects_if_the_particpant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_set_for_the_participant(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(response_set.date_of_birth, self.valid_age)
        self.assertEqual(response_set.participant, self.participant)

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_height_path(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:height"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {"date_of_birth_0": "80000", "date_of_birth_1": "90000", "date_of_birth_2": "20000000"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_create_a_response_set_if_the_user_is_not_in_the_correct_age_range(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.invalid_params
        )

        self.assertEqual(self.participant.responseset_set.first().date_of_birth, None)

    def test_post_redirects_if_the_user_is_not_in_the_correct_age_range(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.invalid_params
        )

        self.assertRedirects(response, reverse("questions:age_range_exit"))
