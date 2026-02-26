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

  Scenario: When I say that I have increased the amount I smoke I am shown the correct page when I am on the smoked amount page
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    And I have answered questions showing I have "increased" my level of "Cigarettes" smoking from "10 cigarettes a day"
    And I have answered questions showing I have "increased" my frequency of "Cigarettes" smoking to "Weekly"
    When I go to "/cigarettes-smoked-increased-amount"
    And I fill in "When you smoked more than 10 cigarettes a day, roughly how many cigarettes did you normally smoke a week?" with "10"
    And I submit the form
    Then I am on "/cigarettes-smoked-increased-years"
