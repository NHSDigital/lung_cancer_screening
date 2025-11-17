from behave import given, then
from playwright.sync_api import expect


@then(u'I see a title "{title}"')
def then_I_see_a_title(context, title):
    expect(context.page.locator('.title')).to_have_text(title)
