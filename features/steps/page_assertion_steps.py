from behave import then
from playwright.sync_api import expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

from lung_cancer_screening.questions.presenters.response_set_presenter import ResponseSetPresenter

@then(u'I see a title "{title}"')
def then_i_see_a_title(context, title):
    expect(context.page.locator('.nhsuk-heading-l')).to_have_text(title)

@then(u'I see a back link to "{url}"')
def then_i_see_a_back_link_to(context, url):
    back_link = context.page.locator(".nhsuk-back-link")
    expect(back_link).to_have_count(1)
    expect(back_link).to_have_attribute("href", url)

@then(u'I see responses "{text}"')
def then_i_see_responses(context, text):
    responses = context.page.locator(".responses")
    expect(responses).to_contain_text(text)

@then(u'I see responses "{text}" with a date {years} years ago')
def then_i_see_responses_with_a_date(context, text, years):
    date_of_birth = datetime.now() - relativedelta(years=int(years))
    responses = context.page.locator(".responses")
    expect(responses).to_contain_text(f"{text} {date_of_birth.strftime(ResponseSetPresenter.DATE_FORMAT)}")


@then(u'I see "{response}" as a response to "{question}" under "{section}"')
def then_i_see_a_response_for(context, question, response, section):
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    expect(summary_list_row).to_contain_text(response)

@then(u'I see a date {years} years ago as a response to "{question}" under "{section}"')
def then_i_see_a_date_x_years_ago_response_for(context, question, years, section):
    date = datetime.now() - relativedelta(years=int(years))
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    expect(summary_list_row).to_contain_text(date.strftime(ResponseSetPresenter.DATE_FORMAT))

@then(u'I see "{url}" as a link to change "{question}" under "{section}"')
def then_i_see_a_response_change_link_for(context, question, url, section):
    summary_list_row = find_summary_list_row_for_question(context, question, section)
    change_link = summary_list_row.locator(".nhsuk-summary-list__actions a")
    expect(change_link).to_have_attribute("href", url)


def find_section_named(context, section):
    return context.page.locator(f"section:has-text('{section}')")

def find_summary_list_row_for_question(context, question, section):
    section = find_section_named(context, section)
    return section.locator(f".nhsuk-summary-list__row:has-text('{question}')")
