from behave import then
from playwright.sync_api import expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

from lung_cancer_screening.questions.presenters.response_set_presenter import ResponseSetPresenter

@then(u'I see a title "{title}"')
def then_i_see_a_title(context, title):
    expect(context.page.locator('.title')).to_have_text(title)

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
