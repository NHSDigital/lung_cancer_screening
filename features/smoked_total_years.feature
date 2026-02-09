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
    Then I see a back link to "/types-tobacco-smoking"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "9"
    And I submit the form
    Then I am on "/cigarettes-smoking-frequency"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoked-total-years"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "9"
    And I submit the form
    When I go to "/check-your-answers"
    Then I see "9" as a response to "Total number of years you have smoked cigarettes" under "Smoking history"
    And I see "/cigarettes-smoked-total-years?change=True" as a link to change "Total number of years you have smoked cigarettes" under "Smoking history"
    When I click the link to change "Total number of years you have smoked cigarettes" under "Smoking history"
    Then I am on "/cigarettes-smoked-total-years?change=True"
    And I see "9" filled in for "Roughly how many years have you smoked cigarettes?"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "8"
    And I click "Continue"
    Then I am on "/check-your-answers"
    And I see "8" as a response to "Total number of years you have smoked cigarettes" under "Smoking history"
