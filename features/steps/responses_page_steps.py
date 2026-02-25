from behave import then
from playwright.sync_api import expect
from datetime import datetime
from dateutil.relativedelta import relativedelta


@then(u'I see "{response}" as a response to "{question}" under "{section}"')
def then_i_see_a_response_for(context, question, response, section):
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    expect(summary_list_row).to_contain_text(response)

@then(u'I see a date {years} years ago as a response to "{question}" under "{section}"')
def then_i_see_a_date_x_years_ago_response_for(context, question, years, section):
    date = datetime.now() - relativedelta(years=int(years))
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    expect(summary_list_row).to_contain_text(date.strftime("%-d %B %Y"))

@then(u'I see "{url}" as a link to change "{question}" under "{section}"')
def then_i_see_a_response_change_link_for(context, question, url, section):
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    change_link = summary_list_row.locator(".nhsuk-summary-list__actions a")
    expect(change_link).to_have_attribute("href", url)

@when(u'I click the link to change "{question}" under "{section}"')
def when_i_click_the_link_to_change(context, question, section):
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    change_link = summary_list_row.locator(".nhsuk-summary-list__actions a")
    change_link.click()

@when(u'I click the link to change "{type}" smoking history')
def when_i_click_the_link_to_change_smoking_history(context, type):
    section = find_section_named(context, f"{type} smoking history")
    section.locator("a").click()

def find_section_named(context, section):
    return context.page.locator(f"section:has-text('{section}')")

def find_summary_list_row_for_question(context, question, section):
    section = find_section_named(context, section)
    return section.locator(f".nhsuk-summary-list__row:has-text('{question}')")
