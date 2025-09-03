import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect


class TestQuestionnaire(StaticLiveServerTestCase):

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

    def test_full_questionaire_user_journey(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        page.fill("input[name='participant_id']", participant_id)

        page.click('text=Start now')

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")

        expect(page.locator("legend")).to_have_text(
            "What is your date of birth?")

        page.fill("input[name='day']", "8")
        page.fill("input[name='month']", "9")
        page.fill("input[name='year']", "2000")

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/responses")

        expect(page.locator(".responses")).to_have_text("2000-09-08")
