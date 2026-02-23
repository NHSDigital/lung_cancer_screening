from behave import step
from datetime import datetime

@step("I take a screenshot")
@step("I take a screenshot {value}")
def screenshot(context, value=""):
    context.page.screenshot(
        full_page=True, path=f"screenshots/{datetime.now()}-{value}-screenshot.png"
    )

@step("I print eligibility")
def print_eligibility(context):
    print("Is user eligible?: ", context.current_user.responseset_set.last().is_eligible())
