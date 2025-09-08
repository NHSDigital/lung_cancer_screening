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

    def test_full_questionaire_user_journey(self):
        participant_id = '123'

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        page.fill("input[name='participant_id']", participant_id)

        page.click('text=Start now')

        expect(page).to_have_url(
            f"{self.live_server_url}/have-you-ever-smoked")

        expect(page.locator("legend")).to_have_text(
            "Have you ever smoked?")

        page.get_by_label('Yes').check()

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")

        expect(page.locator("legend")).to_have_text(
            "What is your date of birth?")

        age = datetime.now() - relativedelta(years=55)

        page.get_by_label("Day").fill(str(age.day))
        page.get_by_label("Month").fill(str(age.month))
        page.get_by_label("Year").fill(str(age.year))

        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/responses")

        expect(page.locator(".responses")).to_contain_text(
            age.strftime("Have you ever smoked? True"))
        expect(page.locator(".responses")).to_contain_text(age.strftime("What is your date of birth? %Y-%m-%d"))
