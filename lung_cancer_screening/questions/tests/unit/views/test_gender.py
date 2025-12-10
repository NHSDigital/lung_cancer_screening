from django.test import TestCase
from django.urls import reverse

from lung_cancer_screening.questions.models.response_set import GenderValues
from .helpers.authentication import login_user


class TestGender(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.user.responseset_set.create()
        self.valid_params = { "gender": GenderValues.MALE }


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:gender")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/gender", fetch_redirect_response=False)


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:gender"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:gender"))

        self.assertContains(response, "Which of these best describes you?")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/gender", fetch_redirect_response=False)


    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(response_set.gender, self.valid_params["gender"])
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_to_the_ethnicity_path(self):
        response = self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:ethnicity"))

    def test_post_responds_with_422_if_the_date_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:gender"),
            {"gender": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_renders_the_gender_page_with_an_error_if_the_form_is_invalid(self):
        response = self.client.post(
            reverse("questions:gender"),
            {"gender": "something not in list"}
        )

        self.assertContains(response, "Which of these best describes you?", status_code=422)
        self.assertContains(response, "nhsuk-error-message", status_code=422)
