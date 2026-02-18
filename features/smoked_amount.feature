@SmokingHistory
@SmokedAmount
Feature: Smoked amount page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes" daily
    When I go to "/cigarettes-smoked-amount"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes" daily
    When I go to "/cigarettes-smoked-amount"
    And I click "Continue"
    Then I am on "/cigarettes-smoked-amount"
    And I see a form error "Enter how many cigarettes you currently smoke in a normal day"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes" daily
    When I go to "/cigarettes-smoked-amount"
    Then I see a back link to "/cigarettes-smoking-frequency"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "20"
    And I submit the form
    Then I am on "/cigarettes-smoking-change"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked "Cigarettes" daily
    When I go to "/cigarettes-smoked-amount"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "20"
    And I submit the form
    When I go to "/check-your-answers"
    Then I see "20 cigarettes a day" as a response to "Current cigarette smoking" under "Smoking history"
    And I see "/cigarettes-smoking-frequency?change=True" as a link to change "Current cigarette smoking" under "Smoking history"
    When I click the link to change "Current cigarette smoking" under "Smoking history"
    Then I am on "/cigarettes-smoking-frequency?change=True"
    When I submit the form
    Then I see "20" filled in for "Roughly how many cigarettes do you currently smoke in a normal day?"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "15"
    And I click "Continue"
    Then I am on "/cigarettes-smoking-change?change=True"
    When I go to "/check-your-answers"
    Then I see "15 cigarettes a day" as a response to "Current cigarette smoking" under "Smoking history"
