@CheckNeedAppointment
Feature: Check if you need an appointment page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/check-if-you-need-an-appointment"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/check-if-you-need-an-appointment"
    And I click "Continue"
    Then I am on "/check-if-you-need-an-appointment"
    And I see a form error "Select if you can continue online"
    And there are no accessibility violations

  Scenario: Eligibility exit if needs face to face appointment
    Given I am logged in
    When I go to "/check-if-you-need-an-appointment"
    Then I see a back link to "/date-of-birth"
    When I check "Yes, one or more of these things applies to me and I need a face-to-face appointment" and submit
    Then I am on "/bmi-exit"

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/check-if-you-need-an-appointment"
    Then I see a back link to "/date-of-birth"
    When I check "No, I can continue online" and submit
    Then I am on "/height"


