import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect

from .helpers.user_interaction_helpers import (
    fill_in_and_submit_participant_id
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

    def test_date_of_birth_validation_errors(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        fill_in_and_submit_participant_id(page, participant_id)
        page.goto(f"{self.live_server_url}/date-of-birth")

        expect(page.locator("legend")).to_have_text(
            "What is your date of birth?")

        page.click("text=Continue")

        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Enter your date of birth."
        )

    def test_height_validation_errors(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        fill_in_and_submit_participant_id(page, participant_id)
        page.goto(f"{self.live_server_url}/height")

        page.click("text=Continue")

        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Enter your height."
        )

        page.click("text=Switch to imperial")

        page.click("text=Continue")

        for error in page.locator(".nhsuk-error-message").all():
            expect(error).to_contain_text(
                "Enter your height."
            )
