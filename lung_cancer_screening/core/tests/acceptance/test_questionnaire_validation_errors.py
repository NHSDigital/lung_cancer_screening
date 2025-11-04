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

        page.get_by_label("Centimetre").fill('139.6')
        page.click('text=Continue')
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Height must be between 139.7cm and 243.8 cm"
        )

        page.get_by_label("Centimetre").fill('243.9')
        page.click('text=Continue')
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Height must be between 139.7cm and 243.8 cm"
        )

        page.click("text=Switch to imperial")

        page.click("text=Continue")
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Enter your height."
        )

        page.get_by_label("Feet").fill('5.2')
        page.get_by_label("Inches").fill('2')
        page.click('text=Continue')
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Feet must be in whole numbers"
        )

        page.get_by_label("Feet").fill('5')
        page.get_by_label("Inches").fill('2.2')
        page.click('text=Continue')
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Inches must be in whole numbers"
        )

    def test_weight_validation_errors(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        fill_in_and_submit_participant_id(page, participant_id)
        page.goto(f"{self.live_server_url}/weight")

        page.click("text=Continue")
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Enter your weight."
        )
        # Test weight below minimum
        page.get_by_label("Kilograms").fill('25.3')
        page.click('text=Continue')
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Weight must be between 25.4kg and 317.5kg"
        )

    def test_ethnicity_validation_errors(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        fill_in_and_submit_participant_id(page, participant_id)
        page.goto(f"{self.live_server_url}/ethnicity")

        page.click("text=Continue")
        expect(page.locator(".nhsuk-error-message")).to_contain_text(
            "Select your ethnic background."
        )
