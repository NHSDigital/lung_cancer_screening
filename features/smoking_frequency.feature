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

  Scenario: When I say that I have increased the amount I smoke I am shown the correct page
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    And I have answered questions showing I have "increased" my level of "Cigarettes" smoking from "10 cigarettes a day"
    Then I am on "/cigarettes-smoking-increased-frequency"
    And I see a title "When you smoked more than 10 cigarettes a day, how often did you smoke cigarettes?"
