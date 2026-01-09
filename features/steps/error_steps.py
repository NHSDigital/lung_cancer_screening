from behave import then
from playwright.sync_api import expect


@then(u'I see an error summary "{error_summary}"')
def then_i_see_an_error_summary(context, error_summary):
    expect(context.page.locator('.nhsuk-error-summary')).to_contain_text(error_summary)

@then(u'I see a form error "{error_message}"')
def then_i_see_a_form_error(context, error_message):
    expect(context.page.locator('.nhsuk-error-message')).to_contain_text(error_message)
