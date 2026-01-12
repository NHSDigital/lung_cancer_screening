from behave import when, then
from playwright.sync_api import expect


@when('I go to "{path}"')
def given_i_go_to(context, path):
    context.page.goto(f"{context.live_server_url}{path}")

@when('I click "{text}"')
def when_i_click(context, text):
    context.page.get_by_text(text, exact=True).click()

@then('I am on "{path}"')
def then_i_am_on(context, path):
    expect(context.page).to_have_url(f"{context.live_server_url}{path}")
