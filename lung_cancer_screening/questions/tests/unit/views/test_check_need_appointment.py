from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.check_need_appointment_response import CheckNeedAppointmentResponse
from ...factories.response_set_factory import ResponseSetFactory

@tag("CheckNeedAppointment")
class TestGetCheckNeedAppointment(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:check_need_appointment")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/check-if-you-need-an-appointment", fetch_redirect_response=False)


    def test_get_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:check_need_appointment")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:check_need_appointment"))

        self.assertEqual(response.status_code, 200)


    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:check_need_appointment"))

        self.assertContains(response, "Do you need to leave the online service and ask for a face-to-face appointment?")

@tag("CheckNeedAppointment")
class TestPostCheckNeedAppointment(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": False}


    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/check-if-you-need-an-appointment", fetch_redirect_response=False)


    def test_post_creates_an_unsubmitted_response_set_for_the_user_when_no_response_set_exists(self):
        self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(CheckNeedAppointmentResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_updates_an_unsubmitted_response_set_for_the_user_when_an_unsubmitted_response_set_existso(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(CheckNeedAppointmentResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_creates_an_new_unsubmitted_response_set_for_the_user_when_a_non_recently_submitted_response_set_exists(self):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )

        self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(CheckNeedAppointmentResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:check_need_appointment"),
            self.valid_params
        )

        # Assuming it redirects to the next question page - adjust as needed
        self.assertRedirects(response, reverse("questions:height"))

    def test_post_redirects_to_book_an_appointment_page(self):
        response = self.client.post(
            reverse("questions:check_need_appointment"),
            {"value": True}
        )

        # Assuming it redirects to the next question page - adjust as needed
        self.assertRedirects(response, reverse("questions:book_an_appointment"))

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:check_need_appointment"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:check_need_appointment"),
            {"value": "invalid"}
        )

        response_set = self.user.responseset_set.first()
        if response_set:
            self.assertFalse(CheckNeedAppointmentResponse.objects.filter(response_set=response_set).exists())
