from behave import when
from datetime import datetime

@given("I take a screenshot")
@given("I take a screenshot {value}")
@when("I take a screenshot")
@when("I take a screenshot {value}")
@then("I take a screenshot")
@then("I take a screenshot {value}")
def screenshot(context, value=""):
    context.page.screenshot(
        full_page=True, path=f"screenshots/{datetime.now()}-{value}-screenshot.png"
    )

@given("I print eligibiity")
@when("I print eligibiity")
@then("I print eligibiity")
def print_eligibiity(context):
    print("Is user eligible?: ", context.current_user.responseset_set.last().is_eligible())

