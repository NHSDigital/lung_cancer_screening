from django.test import TestCase
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.asbestos_exposure_response import AsbestosExposureResponse


class TestGetAsbestosExposure(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:asbestos_exposure")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/asbestos-exposure", fetch_redirect_response=False)


    def test_get_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:asbestos_exposure")
        )

        self.assertRedirects(response, reverse("questions:start"))


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertEqual(response.status_code, 200)


    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertContains(response, "Have you ever worked in a job where you might have been exposed to asbestos?")


class TestPostAsbestosExposure(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": True}


    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/asbestos-exposure", fetch_redirect_response=False)


    def test_post_creates_an_unsubmitted_response_set_for_the_user_when_no_response_set_exists(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(AsbestosExposureResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_updates_an_unsubmitted_response_set_for_the_user_when_an_unsubmitted_response_set_existso(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(AsbestosExposureResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_creates_an_new_unsubmitted_response_set_for_the_user_when_an_submitted_response_set_exists_over_a_year_ago(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(AsbestosExposureResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))


    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        # Assuming it redirects to the next question page - adjust as needed
        self.assertEqual(response.status_code, 302)

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            {"value": "invalid"}
        )

        response_set = self.user.responseset_set.first()
        if response_set:
            self.assertFalse(AsbestosExposureResponse.objects.filter(response_set=response_set).exists())
