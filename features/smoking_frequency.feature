@SmokingHistory
@SmokingFrequency
Feature: Smoking frequency page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-frequency"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-frequency"
    And I click "Continue"
    Then I am on "/cigarettes-smoking-frequency"
    And I see a form error "Select how often you smoke cigarettes"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-frequency"
    Then I see a back link to "/cigarettes-smoked-total-years"
    When I check "Daily" and submit
    Then I am on "/cigarettes-smoked-amount"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-frequency"
    And I check "Daily" and submit
    And I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "10"
    And I submit the form
    When I go to "/check-your-answers"
    Then I see "10 cigarettes a day" as a response to "Current cigarette smoking" under "Smoking history"
    And I see "/cigarettes-smoking-frequency?change=True" as a link to change "Current cigarette smoking" under "Smoking history"
    When I click the link to change "Current cigarette smoking" under "Smoking history"
    Then I am on "/cigarettes-smoking-frequency?change=True"
    And I see "Daily" selected
    When I check "Weekly" and submit
    Then I am on "/cigarettes-smoked-amount?change=True"
    When I go to "/check-your-answers"
    Then I see "10 cigarettes a week" as a response to "Current cigarette smoking" under "Smoking history"
