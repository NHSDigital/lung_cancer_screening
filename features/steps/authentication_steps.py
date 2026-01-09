from behave import given
from django.test import Client
from django.conf import settings
from urllib.parse import urlparse

from lung_cancer_screening.questions.tests.factories.user_factory import (
    UserFactory,
)


@given('I am logged in')
def given_i_am_logged_in(context):
    current_user = UserFactory()

    client = Client()
    client.force_login(current_user)

    # Extract the session cookie from the test client
    session_cookie_name = getattr(
        settings, 'SESSION_COOKIE_NAME', 'sessionid'
    )
    session_cookie = client.cookies.get(session_cookie_name)

    parsed_url = urlparse(context.live_server_url)
    domain = parsed_url.hostname
    context.page.context.add_cookies([{
        'name': session_cookie.key,
        'value': session_cookie.value,
        'domain': domain,
        'path': '/',
    }])

    # Store the user in context for potential future use
    context.current_user = current_user
