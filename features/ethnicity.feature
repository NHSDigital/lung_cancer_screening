Feature: Ethnicity page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/ethnicity"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/ethnicity"
    And I click "Continue"
    Then I am on "/ethnicity"
    And I see a form error "Select your ethnic background"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/ethnicity"
    Then I see a back link to "/gender"
    When I fill in and submit my ethnicity with "White"
    Then I am on "/education"

