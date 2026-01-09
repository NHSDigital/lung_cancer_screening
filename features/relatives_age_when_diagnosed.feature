Feature: Relatives age when diagnosed page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"
    And there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"
    When I submit the form
    Then I am on "/relatives-age-when-diagnosed"
    And I see a form error "Select if your relatives were younger than 60 when they were diagnosed with lung cancer"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"
    And I see a back link to "/family-history-lung-cancer"
    When I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"
    Then I am on "/responses"

  Scenario: Redirecting if they have no family history of lung cancer
    Given I am logged in
    When I go to "/relatives-age-when-diagnosed"
    Then I am on "/family-history-lung-cancer"
