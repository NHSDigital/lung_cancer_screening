from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory

@tag("CheckNeedAppointment")
class TestGetCheckNeedAppointment(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = ResponseSetFactory.create(user=self.user)


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:check_need_appointment")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/check-if-you-need-an-appointment", fetch_redirect_response=False)


    def test_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:check_need_appointment")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_if_hasnt_answered_date_of_birth(self):
        response = self.client.get(reverse("questions:check_need_appointment"))

        self.assertRedirects(response, reverse("questions:date_of_birth"), fetch_redirect_response=False)


    def test_redirects_if_has_answered_date_of_birth_with_ineligible_response(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set,
            ineligible=True
        )

        response = self.client.get(reverse("questions:check_need_appointment"))

        self.assertRedirects(response, reverse("questions:date_of_birth"), fetch_redirect_response=False)


    def test_responds_successfully(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set, eligible=True
        )

        response = self.client.get(reverse("questions:check_need_appointment"))

        self.assertEqual(response.status_code, 200)


@tag("CheckNeedAppointment")
class TestPostCheckNeedAppointment(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user)

        self.valid_params = {"value": False}


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/check-if-you-need-an-appointment", fetch_redirect_response=False)


    def test_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_if_hasnt_answered_date_of_birth(self):
        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:date_of_birth"), fetch_redirect_response=False)


    def test_redirects_if_has_answered_date_of_birth_with_ineligible_response(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set, ineligible=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:date_of_birth"), fetch_redirect_response=False)


    def test_redirects_to_the_next_page(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set, eligible=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:height"), fetch_redirect_response=False)


    def test_redirects_to_book_an_appointment_page(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set, eligible=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            {"value": True}
        )

        self.assertRedirects(response, reverse("questions:book_an_appointment"))

    def test_responds_with_422_if_the_response_fails_to_create(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set, eligible=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
