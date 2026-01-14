@Education
Feature: Education page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/education"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/education"
    And I click "Continue"
    Then I am on "/education"
    And I see a form error "Select your level of education"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/education"
    Then I see a back link to "/ethnicity"
    When I fill in and submit my education with "A-levels"
    Then I am on "/respiratory-conditions"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/education"
    And I fill in and submit my education with "A-levels"
    When I go to "/check-your-answers"
    Then I see "A-levels" as a response to "Highest level of education" under "About you"
    And I see "/education?change=True" as a link to change "Highest level of education" under "About you"
    When I click the link to change "Highest level of education" under "About you"
    Then I am on "/education?change=True"
    And I see "A-levels" selected
    When I fill in and submit my education with "GCSEs"
    Then I am on "/check-your-answers"
    And I see "GCSEs" as a response to "Highest level of education" under "About you"

