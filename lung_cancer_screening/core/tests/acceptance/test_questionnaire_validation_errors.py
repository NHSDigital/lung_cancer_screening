import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect

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

        page.fill("input[name='participant_id']", participant_id)

        page.click('text=Start now')

        expect(page).to_have_url(
            f"{self.live_server_url}/have-you-ever-smoked")

        expect(page.locator("legend")).to_have_text(
            "Have you ever smoked?")

        page.get_by_label('Yes, I currently smoke').check()

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")

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
