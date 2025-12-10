from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user

from lung_cancer_screening.questions.models.response_set import EthnicityValues

class TestEthnicity(TestCase):
    def setUp(self):
        self.user =login_user(self.client)

        self.user.responseset_set.create()
        self.valid_params = { "ethnicity": EthnicityValues.WHITE }


### Test GET request
    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:ethnicity")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/ethnicity", fetch_redirect_response=False)


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:ethnicity"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:ethnicity"))

        self.assertContains(response, "What is your ethnic background?")

### Test POST request

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:ethnicity"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/ethnicity", fetch_redirect_response=False)


    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:ethnicity"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(response_set.ethnicity, self.valid_params["ethnicity"])
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_to_the_asbestos_exposure_path(self):
        response = self.client.post(
            reverse("questions:ethnicity"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:education"))

    def test_post_responds_with_422_if_the_date_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:ethnicity"),
            {"ethnicity": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_renders_the_ethnicity_page_with_an_error_if_the_form_is_invalid(self):
        response = self.client.post(
            reverse("questions:ethnicity"),
            {"ethnicity": "something not in list"}
        )

        self.assertContains(response, "What is your ethnic background?", status_code=422)
        self.assertContains(response, "nhsuk-error-message", status_code=422)
