from django.test import TestCase
from django.urls import reverse

from ....models.participant import Participant
from .helpers.authentication import login_user


class TestWeight(TestCase):
    def setUp(self):
        login_user(self.client)

        self.participant = Participant.objects.create(unique_id="12345")
        self.participant.responseset_set.create()

        self.valid_weight = 70
        self.valid_params = {"weight_metric": self.valid_weight}

        self.session = self.client.session
        self.session['participant_id'] = self.participant.unique_id

        self.session.save()

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        participant = Participant.objects.create(unique_id="abcdef")
        self.client.logout()
        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.get(
            reverse("questions:weight")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/weight", fetch_redirect_response=False)


    def test_get_redirects_if_the_participant_does_not_exist(self):
        self.session['participant_id'] = "somebody none existent participant"
        self.session.save()

        response = self.client.get(
            reverse("questions:weight")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_redirects_if_the_participant_is_none(self):
        del self.session['participant_id']
        self.session.save()

        response = self.client.get(
            reverse("questions:weight")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:weight"))

        self.assertEqual(response.status_code, 200)

    def test_get_renders_the_metric_form(self):
        response = self.client.get(reverse("questions:weight"))

        self.assertContains(response, "Kilograms")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()
        participant = Participant.objects.create(unique_id="abcdef")

        session = self.client.session
        session['participant_id'] = participant.unique_id
        session.save()

        response = self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

    def test_post_redirects_if_the_participant_does_not_exist(self):
        self.session['participant_id'] = "somebody none existent participant"
        self.session.save()

        response = self.client.post(
            reverse("questions:weight")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_redirects_if_the_participant_is_none(self):
        del self.session['participant_id']
        self.session.save()

        response = self.client.post(
            reverse("questions:weight")
        )

        self.assertRedirects(response, reverse("questions:start"))


    def test_post_redirects_if_the_weight_is_valid(self):
        response = self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:sex_at_birth"))

    def test_post_valid_weight_added_to_response_set(self):
        self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        response_set = self.participant.responseset_set.first()
        self.assertEqual(response_set.weight_metric, self.valid_weight * 10)


    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:weight"),
            {"weight": "not a valid weight"}
        )

        self.assertEqual(response.status_code, 422)
