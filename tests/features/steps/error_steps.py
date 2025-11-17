from behave import then
from playwright.sync_api import expect


@then(u'I should see an error summary "{error_summary}"')
def then_I_should_see_an_error_summary(context, error_summary):
    expect(context.page.locator('.nhsuk-error-summary')).to_contain_text(error_summary)
