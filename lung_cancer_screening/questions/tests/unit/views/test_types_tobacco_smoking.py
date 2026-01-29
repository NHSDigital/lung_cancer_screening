import humps

from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes


@tag("TypesTobaccoSmoking")
class TestGetTypesTobaccoSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:types_tobacco_smoking")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/types-tobacco-smoking",
            fetch_redirect_response=False
        )


    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:types_tobacco_smoking")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.get(reverse("questions:types_tobacco_smoking"))

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_get_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:types_tobacco_smoking")
        )

        self.assertEqual(response.status_code, 200)


@tag("TypesTobaccoSmoking")
class TestPostTypesTobaccoSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": [TobaccoSmokingHistoryTypes.CIGARETTES.value]}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:types_tobacco_smoking"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/types-tobacco-smoking",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:types_tobacco_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:types_tobacco_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_creates_a_tobacco_smoking_type_parent_model_for_each_type_given(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        self.client.post(
            reverse("questions:types_tobacco_smoking"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(response_set.tobacco_smoking_history.count(), 1)
        self.assertEqual(response_set.tobacco_smoking_history.first().type, TobaccoSmokingHistoryTypes.CIGARETTES.value)


    def test_post_redirects_to_the_first_type_of_tobacco_smoking_history_question(self):
        ResponseSetFactory.create(user=self.user, eligible=True)
        response = self.client.post(
            reverse("questions:types_tobacco_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:smoked_total_years", kwargs={
            "tobacco_type": humps.kebabize(TobaccoSmokingHistoryTypes.CIGARETTES.value)
        }))
