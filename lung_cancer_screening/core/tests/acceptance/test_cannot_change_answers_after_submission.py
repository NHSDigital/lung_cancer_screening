import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .helpers.user_interaction_helpers import (
    fill_in_and_submit_height_metric,
    fill_in_and_submit_participant_id,
    fill_in_and_submit_smoking_eligibility,
    fill_in_and_submit_date_of_birth
)


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

    def test_cannot_change_responses_once_checked_and_submitted(self):
        participant_id = '123'
        smoking_status = 'Yes, I used to smoke regularly'
        age = datetime.now() - relativedelta(years=55)

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)
        fill_in_and_submit_smoking_eligibility(page, smoking_status)
        fill_in_and_submit_date_of_birth(page, age)
        fill_in_and_submit_height_metric(page, "170")

        page.click("text=Submit")

        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)

        expect(page.locator('#maincontent')).to_contain_text(
            "Responses have already been submitted for this participant"
        )
