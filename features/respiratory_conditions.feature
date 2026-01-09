Feature: Respiratory conditions page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/respiratory-conditions"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/respiratory-conditions"
    And I click "Continue"
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions"
    When I fill in and submit my respiratory conditions with "Bronchitis" and "No, I have not had any of these respiratory conditions"
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions, or select 'No, I have not had any of these respiratory conditions'"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/respiratory-conditions"
    Then I see a back link to "/education"
    When I fill in and submit my respiratory conditions with "Pneumonia" and "Emphysema"
    Then I am on "/asbestos-exposure"

