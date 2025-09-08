import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect

from .helpers.user_interaction_helpers import (
    fill_in_and_submit_participant_id,
    fill_in_and_submit_smoking_elligibility,
    fill_in_and_submit_date_of_birth
)

class TestQuestionnaireValidationErrors(StaticLiveServerTestCase):

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

    def test_full_questionaire_user_journey_with_validation_errors(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)
        fill_in_and_submit_smoking_elligibility(page, 'Yes, I currently smoke')

        expect(page.locator("legend")).to_have_text(
            "What is your date of birth?")

        page.get_by_label("Day").fill("100")
        page.get_by_label("Month").fill("100")
        page.get_by_label("Year").fill("some string")

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")

        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Day should be between 1 and 31"
        )
