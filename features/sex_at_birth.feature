Feature: Sex at birth page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/sex-at-birth"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/sex-at-birth"
    And I click "Continue"
    Then I am on "/sex-at-birth"
    And I see a form error "Select your sex at birth"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/sex-at-birth"
    Then I see a back link to "/weight"
    When I fill in and submit my sex at birth with "Male"
    Then I am on "/gender"

