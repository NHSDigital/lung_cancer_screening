Feature: Family history of lung cancer page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    Then there are no accessibility violations
    When I click "Continue"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I click "Continue"
    Then I am on "/family-history-lung-cancer"
    And I see a form error "Select if any of your parents, siblings or children have had a diagnosis of lung cancer"

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    Then I see a back link to "/cancer-diagnosis"
    When I fill in and submit my asbestos exposure with "No"
    Then I am on "/responses"
    When I click "Back"
    When I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"

