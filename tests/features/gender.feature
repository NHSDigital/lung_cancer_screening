Feature: Gender page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/gender"
    Then there are no accessibility violations
    When I click "Continue"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/gender"
    And I click "Continue"
    Then I am on "/gender"
    And I see a form error "Select the option that best describes your gender"

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/gender"
    Then I see a back link to "/sex-at-birth"
    When I fill in and submit my gender with "Female"
    Then I am on "/ethnicity"

