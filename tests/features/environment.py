"""
Behave environment setup for Django tests.
behave-django handles test database setup automatically.
We just need to add live server and Playwright setup.
"""
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

# behave-django automatically handles:
# - Django setup
# - Test database creation
# - Database transactions per scenario


class LiveServer(StaticLiveServerTestCase):
    """Live server for Behave tests - extends Django's StaticLiveServerTestCase."""

    @classmethod
    def setUpClass(cls):
        """Set up live server - called once for all scenarios."""
        super().setUpClass()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def before_all(context):
    """Set up before all tests run."""
    # Set up live server (behave-django handles test database)
    LiveServer.setUpClass()
    context.live_server_url = LiveServer.live_server_url
    context.live_server_class = LiveServer

    # Set up Playwright browser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)


def after_all(context):
    """Clean up after all tests run."""
    # Clean up Playwright
    if hasattr(context, 'browser'):
        context.browser.close()
    if hasattr(context, 'playwright'):
        context.playwright.stop()

    # Tear down live server (behave-django handles test database teardown)
    if hasattr(context, 'live_server_class'):
        LiveServer.tearDownClass()


def before_scenario(context, _scenario):
    """Set up before each scenario."""
    # behave-django automatically handles database transactions per scenario
    context.page = context.browser.new_page()


def after_scenario(context, _scenario):
    """Clean up after each scenario."""
    # Close the page if it exists
    if hasattr(context, 'page'):
        context.page.close()
        del context.page

    # behave-django automatically rolls back database transactions
