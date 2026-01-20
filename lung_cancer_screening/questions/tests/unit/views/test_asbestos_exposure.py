from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.asbestos_exposure_response import AsbestosExposureResponse
from ...factories.response_set_factory import ResponseSetFactory


@tag("AsbestosExposure")
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
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:asbestos_exposure")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertEqual(response.status_code, 200)


    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertContains(response, "Have you ever worked in a job where you might have been exposed to asbestos?")


@tag("AsbestosExposure")
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


    def test_post_creates_an_new_unsubmitted_response_set_for_the_user_when_a_non_recently_submitted_response_set_exists(self):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
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
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_post_redirects_to_cancer_diagnosis(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:cancer_diagnosis"))


    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))


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
