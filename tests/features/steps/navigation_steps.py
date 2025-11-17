from behave import given, then
from playwright.sync_api import expect


@given('the participant is on the "{path}" path')
def given_the_participant_is_on_the_path(context, path):
    context.page = context.browser.new_page()
    context.page.goto(f"{context.live_server_url}{path}")

@then('the participant should be on the "{path}" path')
def then_the_participant_should_be_on_the_path(context, path):
    expect(context.page).to_have_url(f"{context.live_server_url}{path}")
