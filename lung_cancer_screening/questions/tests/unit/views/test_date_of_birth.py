from django.test import TestCase, tag
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.date_of_birth_response import DateOfBirthResponse
from ...factories.response_set_factory import ResponseSetFactory


@tag("DateOfBirth")
class TestGetDateOfBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/date-of-birth",
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
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertEqual(response.status_code, 200)


@tag("DateOfBirth")
class TestPostDateOfBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_age = date.today() - relativedelta(years=55)
        self.valid_params = {
            "value_0": self.valid_age.day,
            "value_1": self.valid_age.month,
            "value_2": self.valid_age.year
        }

        self.invalid_age = date.today() - relativedelta(years=20)
        self.invalid_params = {
            "value_0": self.invalid_age.day,
            "value_1": self.invalid_age.month,
            "value_2": self.invalid_age.year
        }

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/date-of-birth",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(DateOfBirthResponse.objects.get(response_set=response_set).value, self.valid_age)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(DateOfBirthResponse.objects.get(response_set=response_set).value, self.valid_age)
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_not_recently_submitted_exists(  # noqa: E501
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )

        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(DateOfBirthResponse.objects.get(response_set=response_set).value, self.valid_age)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_post_stores_a_valid_response_set_for_the_user(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(DateOfBirthResponse.objects.get(response_set=response_set).value, self.valid_age)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_to_height(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:check_need_appointment"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            {
                "value_0": "80000",
                "value_1": "90000",
                "value_2": "20000000"
            }
        )

        self.assertEqual(response.status_code, 422)


    def test_post_redirects_if_user_not_in_correct_age_range(self):
        response = self.client.post(
            reverse("questions:date_of_birth"),
            self.invalid_params
        )

        self.assertRedirects(response, reverse("questions:age_range_exit"))
