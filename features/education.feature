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

