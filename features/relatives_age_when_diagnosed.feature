@RelativesAgeWhenDiagnosed
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

  @AgeWhenStartedSmoking
  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "Yes"
    Then I am on "/relatives-age-when-diagnosed"
    And I see a back link to "/family-history-lung-cancer"
    When I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"
    Then I am on "/age-when-started-smoking"

  Scenario: Redirecting if they have no family history of lung cancer
    Given I am logged in
    When I go to "/relatives-age-when-diagnosed"
    Then I am on "/family-history-lung-cancer"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/family-history-lung-cancer"
    And I fill in and submit my family history lung cancer with "Yes"
    And I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"
    When I go to "/check-your-answers"
    Then I see "Yes, they were younger than 60" as a response to "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"
    And I see "/relatives-age-when-diagnosed?change=True" as a link to change "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"
    When I click the link to change "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"
    Then I am on "/relatives-age-when-diagnosed?change=True"
    And I see "Yes, they were younger than 60" selected
    When I fill in and submit my relatives age when diagnosed with "No, they were 60 or older"
    Then I am on "/check-your-answers"
    And I see "No, they were 60 or older" as a response to "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"
