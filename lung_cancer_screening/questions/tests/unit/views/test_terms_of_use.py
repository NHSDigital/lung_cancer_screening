from django.test import TestCase, tag
from django.urls import reverse

from ...factories.terms_of_use_response_factory import TermsOfUseResponseFactory

from ....models.terms_of_use_response import TermsOfUseResponse
from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory

@tag("TermsOfUse")
class TestGetAgreeTermsOfUse(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = ResponseSetFactory.create(user=self.user)


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:agree_terms_of_use")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/agree-terms-of-use",
            fetch_redirect_response=False
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:agree_terms_of_use")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_responds_successfully(self):
        TermsOfUseResponseFactory.create(
            response_set=self.response_set, accepted=True
        )

        response = self.client.get(reverse("questions:agree_terms_of_use"))

        self.assertEqual(response.status_code, 200)


@tag("TermsOfUse")
class TestPostAgreeTermsOfUse(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user)

        self.valid_params = {"value": True}


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:agree_terms_of_use"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/agree-terms-of-use", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:agree_terms_of_use"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_to_the_next_page(self):
        TermsOfUseResponseFactory.create(
            response_set=self.response_set, accepted=True
        )

        response = self.client.post(
            reverse("questions:agree_terms_of_use"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"), fetch_redirect_response=False)


    def test_post_creates_an_unsubmitted_response_set_for_the_user_when_no_response_set_exists(self):
        self.client.post(
            reverse("questions:agree_terms_of_use"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()

        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(TermsOfUseResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_responds_with_422_if_the_response_fails_to_create(self):
        TermsOfUseResponseFactory.create(
            response_set=self.response_set, accepted=True
        )

        response = self.client.post(
            reverse("questions:agree_terms_of_use"),
            {"value": False}
        )

        self.assertEqual(response.status_code, 422)
