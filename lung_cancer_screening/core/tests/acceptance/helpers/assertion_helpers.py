from playwright.sync_api import expect


def expect_back_link_to_have_url(page, url):
    back_link = page.locator(".nhsuk-back-link")
    expect(back_link).to_have_count(1)
    expect(back_link).to_have_attribute("href", url)
