from playwright.sync_api import expect

def fill_in_and_submit_participant_id(page, participant_id):
    page.fill("input[name='participant_id']", participant_id)
    page.click('text=Start now')


def fill_in_and_submit_smoking_elligibility(page, smoking_status):
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
