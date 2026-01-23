from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta



from lung_cancer_screening.questions.tests.factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from ...factories.response_set_factory import ResponseSetFactory


from .helpers.authentication import login_user

@tag("AgeWhenStartedSmoking")
class TestGetAgeWhenStartedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/age-when-started-smoking",
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
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )
        self.assertEqual(response.status_code, 200)

@tag("AgeWhenStartedSmoking")
class TestPostAgeWhenStartedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": 18}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/age-when-started-smoking",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:age_when_started_smoking")
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()
        DateOfBirthResponseFactory(
            response_set=response_set
        )

        self.client.post(
            reverse("questions:age_when_started_smoking")
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_submitted_exists_over_year_ago(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )

        self.client.post(
            reverse("questions:age_when_started_smoking")
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_post_redirects_to_responses(self):
        self.response_set = ResponseSetFactory()
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            value=timezone.now() - relativedelta(years=int(60))
        )
        self.user.responseset_set.set({self.response_set})

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        self.response_set = ResponseSetFactory()
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            value=timezone.now() - relativedelta(years=int(60))
        )
        self.user.responseset_set.set({self.response_set})

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))
