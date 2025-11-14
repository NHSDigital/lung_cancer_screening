from playwright.sync_api import expect
from axe_playwright_python.sync_playwright import Axe


def expect_back_link_to_have_url(page, url):
    back_link = page.locator(".nhsuk-back-link")
    expect(back_link).to_have_count(1)
    expect(back_link).to_have_attribute("href", url)


def expect_no_accessibility_violations(page):
    axe = Axe()
    axe_results = axe.run(page)
    violations_msg = (
        f"Found the following accessibility violations: \n"
        f"{axe_results.generate_snapshot()}"
    )
    assert axe_results.violations_count == 0, violations_msg

