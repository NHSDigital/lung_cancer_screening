@SmokingHistory
@SmokingCurrent
Feature: Smoking current page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/cigarettes-smoking-current"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/cigarettes-smoking-current"
    And I click "Continue"
    Then I am on "/cigarettes-smoking-current"
    And I see a form error "Select if you currently smoke cigarettes"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-current"
    Then I see a back link to "/age-when-started-smoking"
    When I check "Yes" and submit
    Then I am on "/cigarettes-smoked-total-years"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-current"
    When I check "Yes" and submit
    When I go to "/check-your-answers"
    Then I see "Yes" as a response to "Do you currently smoke cigarettes?" under "Smoking history"
    And I see "/cigarettes-smoking-current?change=True" as a link to change "Do you currently smoke cigarettes?" under "Smoking history"
    When I click the link to change "Do you currently smoke cigarettes?" under "Smoking history"
    Then I am on "/cigarettes-smoking-current?change=True"
    And I see "Yes" selected
    When I check "No" and submit
    Then I am on "/cigarettes-smoked-total-years?change=True"
    When I go to "/check-your-answers"
    Then I see "No" as a response to "Do you currently smoke cigarettes?" under "Smoking history"
