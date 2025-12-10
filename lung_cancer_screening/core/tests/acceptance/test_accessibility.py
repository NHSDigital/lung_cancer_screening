import os

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag, Client
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

from lung_cancer_screening.questions.tests.factories.user_factory import UserFactory
from .helpers.assertion_helpers import expect_no_accessibility_violations
from .helpers.user_interaction_helpers import setup_user

@tag('accessibility')
class TestQuestionnaireAccessibility(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    def setUp(self):
        self.page = self.browser.new_page()

        current_user = UserFactory()
        current_user.responseset_set.create()

        client = Client()
        client.force_login(current_user)

        # Extract the session cookie from the test client
        session_cookie_name = getattr(
            settings, 'SESSION_COOKIE_NAME', 'sessionid'
        )
        session_cookie = client.cookies.get(session_cookie_name)

        parsed_url = urlparse(self.live_server_url)
        domain = parsed_url.hostname
        self.page.context.add_cookies([{
            'name': session_cookie.key,
            'value': session_cookie.value,
            'domain': domain,
            'path': '/',
        }])


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_start_page_accessibility(self):
        self.page.goto(f"{self.live_server_url}/start")
        expect_no_accessibility_violations(self.page)

    def test_start_page_errors_accessibility(self):
        self.page.goto(f"{self.live_server_url}/start")
        self.page.click("text=Start now")
        expect_no_accessibility_violations(self.page)

    def test_have_you_ever_smoked_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/have-you-ever-smoked")
        expect_no_accessibility_violations(self.page)

    def test_have_you_ever_smoked_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/have-you-ever-smoked")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_date_of_birth_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/date-of-birth")
        expect_no_accessibility_violations(self.page)

    def test_date_of_birth_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/date-of-birth")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_height_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/height")
        expect_no_accessibility_violations(self.page)

    def test_height_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/height")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_height_imperial_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/height?unit=imperial")
        expect_no_accessibility_violations(self.page)

    def test_weight_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/weight")
        expect_no_accessibility_violations(self.page)

    def test_weight_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/weight")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_weight_imperial_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/weight?unit=imperial")
        expect_no_accessibility_violations(self.page)

    def test_weight_imperial_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/weight?unit=imperial")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_sex_at_birth_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/sex-at-birth")
        expect_no_accessibility_violations(self.page)

    def test_sex_at_birth_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/sex-at-birth")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_gender_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/gender")
        expect_no_accessibility_violations(self.page)

    def test_gender_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/gender")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_ethnicity_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/ethnicity")
        expect_no_accessibility_violations(self.page)

    def test_ethnicity_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/ethnicity")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    # def test_education_page_accessibility(self):
    #
    #     setup_user(self.page, self.live_server_url)
    #     self.page.goto(f"{self.live_server_url}/education")
    #     expect_no_accessibility_violations(page)

    # def test_respiratory_conditions_page_accessibility(self):
    #
    #     setup_user(self.page, self.live_server_url)
    #     self.page.goto(f"{self.live_server_url}/respiratory-conditions")
    #     expect_no_accessibility_violations(page)

    def test_asbestos_exposure_page_errors_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/asbestos-exposure")
        self.page.click("text=Continue")
        expect_no_accessibility_violations(self.page)

    def test_asbestos_exposure_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/asbestos-exposure")
        expect_no_accessibility_violations(self.page)

    # def test_cancer_diagnosis_page_accessibility(self):
    #
    #     setup_user(self.page, self.live_server_url)
    #     self.page.goto(f"{self.live_server_url}/cancer-diagnosis")
    #     expect_no_accessibility_violations(page)

    # def test_family_history_lung_cancer_page_accessibility(self):
    #
    #     setup_user(self.page, self.live_server_url)
    #     self.page.goto(f"{self.live_server_url}/family-history-lung-cancer")
    #     expect_no_accessibility_violations(page)

    def test_responses_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/responses")
        expect_no_accessibility_violations(self.page)

    def test_your_results_page_accessibility(self):
        setup_user(self.page, self.live_server_url)
        self.page.goto(f"{self.live_server_url}/your-results")
        expect_no_accessibility_violations(self.page)
