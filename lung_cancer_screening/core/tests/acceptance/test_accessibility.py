import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

from .helpers.user_interaction_helpers import setup_participant
from .helpers.assertion_helpers import expect_no_accessibility_violations

class TestQuestionnaireAccessibility(StaticLiveServerTestCase):

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

    def test_start_page_accessibility(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        expect_no_accessibility_violations(page)

    def test_start_page_errors_accessibility(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/start")
        page.click("text=Start now")
        expect_no_accessibility_violations(page)

    def test_have_you_ever_smoked_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/have-you-ever-smoked")
        expect_no_accessibility_violations(page)

    def test_have_you_ever_smoked_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/have-you-ever-smoked")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_date_of_birth_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/date-of-birth")
        expect_no_accessibility_violations(page)

    def test_date_of_birth_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/date-of-birth")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_height_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/height")
        expect_no_accessibility_violations(page)

    def test_height_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/height")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_height_imperial_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/height?unit=imperial")
        expect_no_accessibility_violations(page)

    def test_weight_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/weight")
        expect_no_accessibility_violations(page)

    def test_weight_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/weight")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_weight_imperial_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/weight?unit=imperial")
        expect_no_accessibility_violations(page)

    def test_weight_imperial_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/weight?unit=imperial")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_sex_at_birth_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/sex-at-birth")
        expect_no_accessibility_violations(page)

    def test_sex_at_birth_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/sex-at-birth")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_gender_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/gender")
        expect_no_accessibility_violations(page)

    def test_gender_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/gender")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_ethnicity_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/ethnicity")
        expect_no_accessibility_violations(page)

    def test_ethnicity_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/ethnicity")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    # def test_education_page_accessibility(self):
    #     page = self.browser.new_page()
    #     setup_participant(page, self.live_server_url)
    #     page.goto(f"{self.live_server_url}/education")
    #     expect_no_accessibility_violations(page)

    # def test_respiratory_conditions_page_accessibility(self):
    #     page = self.browser.new_page()
    #     setup_participant(page, self.live_server_url)
    #     page.goto(f"{self.live_server_url}/respiratory-conditions")
    #     expect_no_accessibility_violations(page)

    def test_asbestos_exposure_page_errors_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/asbestos-exposure")
        page.click("text=Continue")
        expect_no_accessibility_violations(page)

    def test_asbestos_exposure_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/asbestos-exposure")
        expect_no_accessibility_violations(page)

    # def test_cancer_diagnosis_page_accessibility(self):
    #     page = self.browser.new_page()
    #     setup_participant(page, self.live_server_url)
    #     page.goto(f"{self.live_server_url}/cancer-diagnosis")
    #     expect_no_accessibility_violations(page)

    # def test_family_history_lung_cancer_page_accessibility(self):
    #     page = self.browser.new_page()
    #     setup_participant(page, self.live_server_url)
    #     page.goto(f"{self.live_server_url}/family-history-lung-cancer")
    #     expect_no_accessibility_violations(page)

    def test_responses_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/responses")
        expect_no_accessibility_violations(page)

    def test_your_results_page_accessibility(self):
        page = self.browser.new_page()
        setup_participant(page, self.live_server_url)
        page.goto(f"{self.live_server_url}/your-results")
        expect_no_accessibility_violations(page)
