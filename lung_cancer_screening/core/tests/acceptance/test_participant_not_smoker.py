import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect


from .helpers.user_interaction_helpers import (
    fill_in_and_submit_participant_id,
    fill_in_and_submit_smoking_eligibility
)


class TestParticipantNotSmoker(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_participant_not_smoker(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)
        fill_in_and_submit_smoking_eligibility(page, 'No, I have never smoked')

        expect(page).to_have_url(f"{self.live_server_url}/non-smoker-exit")

        expect(page.locator(".title")).to_have_text(
            "You do not need an NHS lung health check")
