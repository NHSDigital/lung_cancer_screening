import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .helpers.user_interaction_helpers import (
    fill_in_and_submit_height_imperial,
    fill_in_and_submit_height_metric,
    fill_in_and_submit_participant_id,
    fill_in_and_submit_smoking_eligibility,
    fill_in_and_submit_date_of_birth,
    fill_in_and_submit_weight_metric,
    fill_in_and_submit_weight_imperial,
    fill_in_and_submit_sex_at_birth,
    fill_in_and_submit_gender,
    fill_in_and_submit_ethnicity,
    fill_in_and_submit_asbestos_exposure
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

    def test_full_questionnaire_user_journey(self):
        participant_id = '123'
        smoking_status = 'Yes, I used to smoke regularly'
        age = datetime.now() - relativedelta(years=55)
        height = "170"
        feet = 5
        inches = 7
        weight_metric = 70
        weight_stone = 5
        weight_pound = 10

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")

        fill_in_and_submit_participant_id(page, participant_id)

        expect(page).to_have_url(
            f"{self.live_server_url}/have-you-ever-smoked")
        expect_back_link_to_have_url(page, "/start")
        fill_in_and_submit_smoking_eligibility(page, smoking_status)

        expect(page).to_have_url(f"{self.live_server_url}/date-of-birth")
        expect_back_link_to_have_url(page, "/have-you-ever-smoked")
        fill_in_and_submit_date_of_birth(page, age)

        expect(page).to_have_url(f"{self.live_server_url}/height")
        expect_back_link_to_have_url(page, "/date-of-birth")
        fill_in_and_submit_height_metric(page, height)

        page.click("text=Back")
        expect(page).to_have_url(f"{self.live_server_url}/height")
        page.click("text=Switch to imperial")
        fill_in_and_submit_height_imperial(page, feet, inches)

        expect(page).to_have_url(f"{self.live_server_url}/weight")
        expect_back_link_to_have_url(page, "/height")
        fill_in_and_submit_weight_metric(page, weight_metric)
        page.click("text=Back")

        expect(page).to_have_url(f"{self.live_server_url}/weight")
        page.get_by_role("link", name="Switch to stone and pounds").click()
        fill_in_and_submit_weight_imperial(page, weight_stone, weight_pound)

        expect(page).to_have_url(f"{self.live_server_url}/sex-at-birth")
        expect_back_link_to_have_url(page, "/weight")
        fill_in_and_submit_sex_at_birth(page, "Male")

        expect(page).to_have_url(f"{self.live_server_url}/gender")
        expect_back_link_to_have_url(page, "/sex-at-birth")
        fill_in_and_submit_gender(page, "Male")

        expect(page).to_have_url(f"{self.live_server_url}/ethnicity")
        expect_back_link_to_have_url(page, "/gender")
        fill_in_and_submit_ethnicity(page, "White")

        expect(page).to_have_url(f"{self.live_server_url}/education")
        expect_back_link_to_have_url(page, "/ethnicity")
        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/respiratory-conditions")
        expect_back_link_to_have_url(page, "/education")
        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/asbestos-exposure")
        expect_back_link_to_have_url(page, "/respiratory-conditions")
        fill_in_and_submit_asbestos_exposure(page, "No")

        expect(page).to_have_url(f"{self.live_server_url}/cancer-diagnosis")
        expect_back_link_to_have_url(page, "/asbestos-exposure")
        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/family-history-lung-cancer")
        expect_back_link_to_have_url(page, "/cancer-diagnosis")
        page.click("text=Continue")

        expect(page).to_have_url(f"{self.live_server_url}/responses")
        expect_back_link_to_have_url(page, "/family-history-lung-cancer")

        responses = page.locator(".responses")
        expect(responses).to_contain_text("Have you ever smoked? Yes, I used to smoke regularly")
        expect(responses).to_contain_text(age.strftime("What is your date of birth? %Y-%m-%d"))
        expect(responses).to_contain_text(f"What is your height? {feet} feet {inches} inches")
        expect(responses).to_contain_text(f"What is your weight? {weight_stone} stone {weight_pound} pound")
        expect(responses).to_contain_text("What was your sex at birth? Male")
        expect(responses).to_contain_text("Which of these best describes you? Male")
        expect(responses).to_contain_text("What is your ethnic background? White")
        expect(responses).to_contain_text("Have you ever worked in a job where you might have been exposed to asbestos? No")

        page.click("text=Submit")

        expect(page).to_have_url(f"{self.live_server_url}/your-results")
