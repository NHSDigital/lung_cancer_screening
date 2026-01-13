from behave import then
from playwright.sync_api import expect

@then(u'I see a title "{title}"')
def then_i_see_a_title(context, title):
    expect(context.page.locator('.nhsuk-heading-l')).to_have_text(title)

@then(u'I see a back link to "{url}"')
def then_i_see_a_back_link_to(context, url):
    back_link = context.page.locator(".nhsuk-back-link")
    expect(back_link).to_have_count(1)
    expect(back_link).to_have_attribute("href", url)
