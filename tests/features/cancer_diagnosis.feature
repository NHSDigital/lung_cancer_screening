Feature: Cancer diagnosis page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/cancer-diagnosis"
    Then there are no accessibility violations
    When I click "Continue"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/cancer-diagnosis"
    And I click "Continue"
    Then I am on "/cancer-diagnosis"
    And I see a form error "Select if you have been diagnosed with cancer"

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/cancer-diagnosis"
    Then I see a back link to "/asbestos-exposure"
    When I fill in and submit my asbestos exposure with "No"
    Then I am on "/family-history-lung-cancer"

