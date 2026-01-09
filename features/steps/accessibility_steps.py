from behave import then
from axe_playwright_python.sync_playwright import Axe

@then('there are no accessibility violations')
def then_there_are_no_accessibility_violations(context):
    axe = Axe()
    axe_results = axe.run(context.page)
    violations_msg = (
        f"Found the following accessibility violations: \n"
        f"{axe_results.generate_snapshot()}"
    )
    assert axe_results.violations_count == 0, violations_msg
