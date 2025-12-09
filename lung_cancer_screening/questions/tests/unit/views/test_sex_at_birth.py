from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.participant import Participant
from lung_cancer_screening.questions.models.response_set import SexAtBirthValues

class TestSexAtBirth(TestCase):
    def setUp(self):
        login_user(self.client)

        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()
        self.valid_params = { "sex_at_birth": SexAtBirthValues.FEMALE }

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
            reverse("questions:sex_at_birth")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/sex-at-birth", fetch_redirect_response=False)

    def test_get_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.get(
            reverse("questions:sex_at_birth")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:sex_at_birth"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:sex_at_birth"))

        self.assertContains(response, "What was your sex at birth?")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()
        participant = Participant.objects.create(unique_id="abcdef")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/sex-at-birth", fetch_redirect_response=False)

    def test_post_redirects_if_the_participant_does_not_exist(self):
        session = self.client.session
        session['participant_id'] = "somebody none existant participant"
        session.save()

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_for_the_participant(self):
        self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(response_set.sex_at_birth, self.valid_params["sex_at_birth"])
        self.assertEqual(response_set.participant, self.participant)

    def test_post_sets_the_participant_id_in_session(self):
        self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertEqual(self.client.session["participant_id"], "12345")

    def test_post_redirects_to_the_responses_path(self):
        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:gender"))

    def test_post_responds_with_422_if_the_date_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:sex_at_birth"),
            {"sex_at_birth": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_renders_the_sex_at_birth_page_with_an_error_if_the_form_is_invalid(self):
        response = self.client.post(
            reverse("questions:sex_at_birth"),
            {"sex_at_birth": "something not in list"}
        )

        self.assertContains(response, "What was your sex at birth?", status_code=422)
        self.assertContains(response, "nhsuk-error-message", status_code=422)
