@FamilyHistoryLungCancer
Feature: Family history of lung cancer page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/family-history-lung-cancer"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/family-history-lung-cancer"
    And I click "Continue"
    Then I am on "/family-history-lung-cancer"
    And I see a form error "Select if any of your parents, siblings or children have had a diagnosis of lung cancer"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/family-history-lung-cancer"
    Then I see a back link to "/cancer-diagnosis"
    When I fill in and submit my family history lung cancer with "No"
    Then I am on "/age-when-started-smoking"
    When I click "Back"
    When I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "No"
    When I go to "/check-your-answers"
    Then I see "No" as a response to "Have any of your parents, siblings or children ever been diagnosed with lung cancer? " under "Family history"
    And I see "/family-history-lung-cancer?change=True" as a link to change "Have any of your parents, siblings or children ever been diagnosed with lung cancer? " under "Family history"
    When I click the link to change "Have any of your parents, siblings or children ever been diagnosed with lung cancer? " under "Family history"
    Then I am on "/family-history-lung-cancer?change=True"
    And I see "No" selected
    When I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed?change=True"
    When I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"
    Then I am on "/check-your-answers"
    And I see "Yes" as a response to "Have any of your parents, siblings or children ever been diagnosed with lung cancer? " under "Family history"
    And I see "Yes, they were younger than 60" as a response to "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"
