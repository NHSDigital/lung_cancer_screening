import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .helpers.user_interaction_helpers import (
    fill_in_and_submit_participant_id,
    fill_in_and_submit_smoking_elligibility,
    fill_in_and_submit_date_of_birth
)

from .helpers.assertion_helpers import expect_back_link_to_have_url

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
        smoking_status = 'Yes, I used to smoke regularly'
        age = datetime.now() - relativedelta(years=55)

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)

        expect(page).to_have_url(
            f"{self.live_server_url}/have-you-ever-smoked")

        fill_in_and_submit_smoking_elligibility(page, smoking_status)

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")
        expect_back_link_to_have_url(page, "/have-you-ever-smoked")

        fill_in_and_submit_date_of_birth(page, age)

        expect(page).to_have_url(f"{self.live_server_url}/responses")

        expect(page.locator(".responses")).to_contain_text(
            age.strftime("Have you ever smoked? Yes, I used to smoke regularly"))
        expect(page.locator(".responses")).to_contain_text(age.strftime("What is your date of birth? %Y-%m-%d"))

        page.click("text=Submit")

        expect(page).to_have_url(f"{self.live_server_url}/your-results")
