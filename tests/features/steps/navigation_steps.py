from behave import when, then
from playwright.sync_api import expect


@when('I go to "{path}"')
def given_I_go_to(context, path):
    context.page.goto(f"{context.live_server_url}{path}")

@then('I am on "{path}"')
def then_I_am_on(context, path):
    expect(context.page).to_have_url(f"{context.live_server_url}{path}")
