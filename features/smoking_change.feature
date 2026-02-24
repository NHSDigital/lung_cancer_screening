@SmokingChange
Feature: Smoking change page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    When I go to "/cigarettes-smoking-change"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    When I go to "/cigarettes-smoking-change"
    And I submit the form
    Then I see a form error "Select if the number of cigarettes you smoke has changed over time"
    When I check "Yes, I used to smoke more than 10 cigarettes a day"
    And I check "No, it has not changed"
    And I submit the form
    Then I see a form error "Select if the number of cigarettes you smoke has changed over time, or select 'no, it has not changed'"
    Then there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    When I go to "/cigarettes-smoking-change"
    Then I see a back link to "/cigarettes-smoked-amount"
    When I check "No, it has not changed"
    And I submit the form
    Then I am on "/check-your-answers"
    When I click "Back"
    Then I am on "/cigarettes-smoking-change"
    When I uncheck "No, it has not changed"
    And I check "Yes, I used to smoke more than 10 cigarettes a day"
    And I submit the form
    Then I am on "/cigarettes-smoking-increased-frequency"

