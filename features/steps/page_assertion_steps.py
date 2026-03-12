from behave import then
from playwright.sync_api import expect

@then(u'I see a title "{title}"')
def then_i_see_a_title(context, title):
    expect(context.page.locator('h1')).to_have_text(title)

@then(u'I see a back link to "{url}"')
def then_i_see_a_back_link_to(context, url):
    back_link = context.page.locator(".nhsuk-back-link")
    expect(back_link).to_have_count(1)
    expect(back_link).to_have_attribute("href", url)

@then(u'I see a page title "{title}"')
def then_i_see_a_page_title(context, title):
    expect(context.page.locator('h1')).to_have_text(title)

@then(u'I see a phase header "{phase}"')
def then_i_see_a_phase_header(context, phase):
    expect(context.page.locator('.lung-nhsuk-phase-banner__text')).to_have_count(1)
    expect(context.page.locator('.nhsuk-tag')).to_have_text(phase)

@then(u'I see a link named "{link_text}"')
def then_i_see_a_link_named(context, link_text):
    link = context.page.locator(f'a:has-text("{link_text}")')
    expect(link).to_have_count(1)
