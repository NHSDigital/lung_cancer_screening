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


@step("I print smoking history")
def print_smoking_history(context):
    histories = context.current_user.responseset_set.last().tobacco_smoking_history.all()
    print("Smoking history: ", histories.count())
    for history in histories:
        print("\nHistory: ", history.type, history.level)
