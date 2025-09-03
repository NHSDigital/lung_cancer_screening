import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

    def test_participant_out_of_age_range(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        page.fill("input[name='participant_id']", participant_id)

        page.click('text=Start now')

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")

        expect(page.locator("legend")).to_have_text(
            "What is your date of birth?")

        age = datetime.now() - relativedelta(years=20)

        page.fill("input[name='day']", str(age.day))
        page.fill("input[name='month']", str(age.month))
        page.fill("input[name='year']", str(age.year))

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/age-range-exit")

        expect(page.locator(".title")).to_have_text(
            "You do not need an NHS lung health check")
