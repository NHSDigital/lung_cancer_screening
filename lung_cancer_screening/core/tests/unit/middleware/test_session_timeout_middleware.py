import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

SESSION_START_KEY = "_session_start_"
LAST_ACTIVITY_KEY = "_last_activity_"


class TestSessionTimeoutMiddleware(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(nhs_number='1234567890')
        self.client.force_login(self.user)
        self.logged_in_url = reverse("questions:have_you_ever_smoked")


    def test_does_nothing_if_there_is_no_session(self):
        self.client.session.flush()

        self.client.get(reverse("questions:start"))

        session = self.client.session
        self.assertNotIn(LAST_ACTIVITY_KEY, session)
        self.assertNotIn(SESSION_START_KEY, session)


    def test_does_nothing_if_the_user_is_not_authenticated(self):
        self.client.logout()

        self.client.get(reverse("questions:start"))

        session = self.client.session
        self.assertNotIn(LAST_ACTIVITY_KEY, session)
        self.assertNotIn(SESSION_START_KEY, session)


    def test_last_activity_set_on_first_request(self):
        session = self.client.session
        self.assertNotIn(LAST_ACTIVITY_KEY, session)

        self.client.get(reverse("questions:start"))

        session = self.client.session
        self.assertIn(LAST_ACTIVITY_KEY, session)

    def test_updates_last_activity_on_each_request(self):
        session = self.client.session
        old_activity = time.time()
        session[LAST_ACTIVITY_KEY] = old_activity
        session.save()

        self.client.get(self.logged_in_url)

        session = self.client.session
        new_activity = session[LAST_ACTIVITY_KEY]
        self.assertGreater(new_activity, old_activity)


    def test_session_start_set_on_first_request(self):
        session = self.client.session
        self.assertNotIn(SESSION_START_KEY, session)

        self.client.get(self.logged_in_url)

        session = self.client.session
        self.assertIn(SESSION_START_KEY, session)


    def test_session_start_not_updated_on_each_request(self):
        session = self.client.session
        original_start = time.time()
        session[SESSION_START_KEY] = original_start
        session.save()

        self.client.get(self.logged_in_url)

        session = self.client.session
        self.assertEqual(session[SESSION_START_KEY], original_start)


    def test_session_expires_after_30_minute_inactivity(self):
        session = self.client.session
        session[SESSION_START_KEY] = time.time() - (1 * 3600)
        session[LAST_ACTIVITY_KEY] = time.time() - (31 * 60)
        session.save()

        response = self.client.get(self.logged_in_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGOUT_REDIRECT_URL)

    def test_session_expires_after_12_hour_continuous_usage(self):
        session = self.client.session
        session[SESSION_START_KEY] = time.time() - (13 * 3600)
        session[LAST_ACTIVITY_KEY] = time.time() - (5 * 60)
        session.save()

        response = self.client.get(self.logged_in_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGOUT_REDIRECT_URL)

    def test_session_valid_within_both_limits(self):
        session = self.client.session
        session[SESSION_START_KEY] = time.time() - (11 * 3600)
        session[LAST_ACTIVITY_KEY] = time.time() - (25 * 60)
        session.save()

        response = self.client.get(self.logged_in_url)

        self.assertEqual(response.status_code, 200)
