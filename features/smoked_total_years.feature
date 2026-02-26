@SmokingHistory
@SmokedTotalYears
Feature: Smoked total years page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoked-total-years"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoked-total-years"
    And I click "Continue"
    Then I am on "/cigarettes-smoked-total-years"
    And I see a form error "Enter the number of years you have smoked cigarettes"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoked-total-years"
    Then I see a back link to "/cigarettes-smoking-current"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "9"
    And I submit the form
    Then I am on "/cigarettes-smoking-frequency"

  Scenario: When I say that I have increased the amount I smoke I am shown the correct page when I am on the smoked total years page
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I currently smoke "Cigarettes"
    And I have answered questions showing I have smoked 10 "Cigarettes" "daily"
    And I have answered questions showing I have "increased" my level of "Cigarettes" smoking from "10 cigarettes a day"
    And I have answered questions showing I have "increased" my frequency of "Cigarettes" smoking to "Weekly"
    And I have answered questions showing I have "increased" my amount of "Cigarettes" smoking to "10"
    When I go to "/cigarettes-smoked-increased-years"
    And I fill in "Roughly how many years did you smoke 10 cigarettes a week?" with "9"
    And I submit the form
    Then I am on "/check-your-answers"
