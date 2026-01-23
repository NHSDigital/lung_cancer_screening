from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.sex_at_birth_response import SexAtBirthValues
from ...factories.response_set_factory import ResponseSetFactory


@tag("SexAtBirth")
class TestGetSexAtBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:sex_at_birth")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/sex-at-birth",
            fetch_redirect_response=False
        )

    def test_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:sex_at_birth")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:sex_at_birth")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:sex_at_birth"))

        self.assertEqual(response.status_code, 200)


@tag("SexAtBirth")
class TestPostSexAtBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": SexAtBirthValues.FEMALE}

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/sex-at-birth",
            fetch_redirect_response=False
        )

    def test_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_creates_a_sex_at_birth_response(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        self.client.post(reverse("questions:sex_at_birth"), self.valid_params)

        response_set.refresh_from_db()
        self.assertEqual(
            response_set.sex_at_birth_response.value, self.valid_params["value"]
        )

    def test_redirects_to_gender(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:gender"))

    def test_redirects_to_responses_if_change_query_param_is_true(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_responds_with_422_if_the_response_fails_to_create(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:sex_at_birth"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
