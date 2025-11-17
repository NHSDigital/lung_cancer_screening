from behave import then
from playwright.sync_api import expect


@then(u'the participant should see en error summary "{error_summary}"')
def then_the_participant_should_see_an_error_summary(context, error_summary):
    expect(context.page.locator('#maincontent')).to_contain_text(error_summary)
