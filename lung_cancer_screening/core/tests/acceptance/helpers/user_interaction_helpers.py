from playwright.sync_api import expect
from .test_helpers import check_labels

def setup_user(page, live_server_url):
    user_id = 'abc123'
    page.goto(f"{live_server_url}/start")
    fill_in_and_submit_user_id(page, user_id)

def fill_in_and_submit_user_id(page, user_id):
    page.fill("input[name='user_id']", user_id)
    page.click('text=Start now')


def fill_in_and_submit_smoking_eligibility(page, smoking_status):
    expect(page.locator("legend")).to_have_text(
        "Have you ever smoked?")

    page.get_by_label(smoking_status).check()

    page.click("text=Continue")

def fill_in_and_submit_date_of_birth(page, age):
    expect(page.locator("legend")).to_have_text(
        "What is your date of birth?")

    page.get_by_label("Day").fill(str(age.day))
    page.get_by_label("Month").fill(str(age.month))
    page.get_by_label("Year").fill(str(age.year))

    page.click("text=Continue")

def fill_in_and_submit_height_metric(page, height):
    expect(page.locator("h1")).to_have_text("What is your height?")

    page.get_by_label("Centimetre").fill(str(height))

    page.click("text=Continue")

def fill_in_and_submit_height_imperial(page, feet, inches):
    expect(page.locator("h1")).to_have_text("What is your height?")

    page.get_by_label("Feet").fill(str(feet))
    page.get_by_label("Inches").fill(str(inches))

    page.click("text=Continue")

def fill_in_and_submit_weight_metric(page, kilograms):
    expect(page.locator("h1")).to_have_text("Enter your weight")

    page.get_by_label("Kilograms").fill(str(kilograms))

    page.click("text=Continue")

def fill_in_and_submit_weight_imperial(page, stone, pounds):
    expect(page.locator("h1")).to_have_text("Enter your weight")

    page.get_by_label("Stone").fill(str(stone))
    page.get_by_label("Pounds").fill(str(pounds))

    page.click("text=Continue")

def fill_in_and_submit_sex_at_birth(page, sex):
    expect(page.locator("legend")).to_have_text(
        "What was your sex at birth?")

    page.get_by_label(sex, exact=True).check()

    page.click("text=Continue")

def fill_in_and_submit_gender(page, gender):
    expect(page.locator("legend")).to_have_text(
        "Which of these best describes you?")

    page.get_by_label(gender, exact=True).check()

    page.click("text=Continue")

def fill_in_and_submit_ethnicity(page, ethnicity):
    expect(page.locator("legend")).to_have_text(
        "What is your ethnic background?")

    page.get_by_label(ethnicity, exact=True).check()

    page.click("text=Continue")

def fill_in_and_submit_asbestos_exposure(page, answer):
    expect(page.locator("legend")).to_have_text(
        "Have you ever worked in a job where you might have been exposed to asbestos?")

    page.get_by_label(answer, exact=True).check()

    page.click("text=Continue")

def fill_in_and_submit_respiratory_conditions(page, answer):
    expect(page.locator("legend")).to_have_text(
        "Have you ever been diagnosed with any of the following respiratory conditions?")

    check_labels(page, answer)

    page.click("text=Continue")

