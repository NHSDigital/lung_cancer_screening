from django.test import TestCase
from django.urls import reverse
from datetime import date

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from .helpers.authentication import login_user


class TestGetResponses(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/check-your-answers",
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
            reverse("questions:responses")
        )

        self.assertRedirects(
            response, reverse("questions:confirmation")
        )


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_get_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:responses"))

        self.assertEqual(response.status_code, 200)


    def test_get_contains_the_users_responses(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertContains(response, response_set.date_of_birth_response.value.strftime("%-d %B %Y"))


    def test_get_does_not_contain_responses_for_other_users(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        other_response_set = ResponseSetFactory.create()
        DateOfBirthResponseFactory.create(response_set=other_response_set, value=date(1990, 1, 1))

        response = self.client.get(reverse("questions:responses"))

        self.assertNotContains(
            response, other_response_set.date_of_birth_response.value.strftime("%-d %B %Y")
        )


class TestPostResponses(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/check-your-answers",
            fetch_redirect_response=False
        )

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:responses")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_post_responds_with_422_if_the_response_set_is_not_complete(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(reverse("questions:responses"))

        self.assertEqual(response.status_code, 422)


    def test_post_redirects_to_confirmation(self):
        ResponseSetFactory.create(user=self.user, complete=True)

        response = self.client.post(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:confirmation"), fetch_redirect_response=False)


    def test_post_marks_the_result_set_as_submitted(self):
        response_set = ResponseSetFactory.create(user=self.user, complete=True)

        self.client.post(reverse("questions:responses"))

        response_set.refresh_from_db()
        self.assertIsNotNone(
            response_set.submitted_at
        )
