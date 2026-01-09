Feature: Asbestos exposure page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/asbestos-exposure"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/asbestos-exposure"
    And I click "Continue"
    Then I am on "/asbestos-exposure"
    And I see a form error "Select if you have been exposed to asbestos"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/asbestos-exposure"
    Then I see a back link to "/respiratory-conditions"
    When I fill in and submit my asbestos exposure with "No"
    Then I am on "/cancer-diagnosis"

