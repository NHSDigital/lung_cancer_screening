from django.test import TestCase, tag
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.have_you_ever_smoked_response import (
    HaveYouEverSmokedValues,
)
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory


@tag("DateOfBirth")
class TestGetDateOfBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = ResponseSetFactory.create(
            user=self.user,
        )
        self.response = HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY,
        )

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/date-of-birth",
            fetch_redirect_response=False
        )

    def test_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:date_of_birth")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_to_have_you_ever_smoked_if_the_user_hasnt_answered_have_you_ever_smoked(self):
        self.response.delete()
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_redirects_to_have_you_ever_smoked_if_the_user_has_answered_have_you_ever_smoked_with_no(self):
        self.response.value = HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED
        self.response.save()

        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertEqual(response.status_code, 200)


@tag("DateOfBirth")
class TestPostDateOfBirth(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = ResponseSetFactory.create(
            user=self.user,
        )
        self.response = HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY,
        )

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


    def test_redirects_when_submitted_response_set_exists_within_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.post(reverse("questions:date_of_birth"), self.valid_params)

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_to_have_you_ever_smoked_if_the_user_hasnt_answered_have_you_ever_smoked(
        self,
    ):
        self.response.delete()
        response = self.client.post(reverse("questions:date_of_birth"), self.valid_params)

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_redirects_to_have_you_ever_smoked_if_the_user_has_answered_have_you_ever_smoked_with_no(
        self,
    ):
        self.response.value = HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED
        self.response.save()

        response = self.client.get(reverse("questions:date_of_birth"))

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_creates_a_date_of_birth_response(self):
        self.client.post(
            reverse("questions:date_of_birth"),
            self.valid_params
        )

        self.response_set.refresh_from_db()
        self.assertEqual(self.response_set.date_of_birth_response.value, self.valid_age)


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

        self.assertRedirects(response, reverse("questions:responses"), fetch_redirect_response=False)

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
