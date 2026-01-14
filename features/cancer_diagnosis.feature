@CancerDiagnosis
Feature: Cancer diagnosis page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/cancer-diagnosis"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/cancer-diagnosis"
    And I click "Continue"
    Then I am on "/cancer-diagnosis"
    And I see a form error "Select if you have been diagnosed with cancer"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/cancer-diagnosis"
    Then I see a back link to "/asbestos-exposure"
    When I fill in and submit my cancer diagnosis with "No"
    Then I am on "/family-history-lung-cancer"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/cancer-diagnosis"
    And I fill in and submit my cancer diagnosis with "No"
    When I go to "/check-your-answers"
    Then I see "No" as a response to "Have you ever been diagnosed with cancer?" under "Your health"
    And I see "/cancer-diagnosis?change=True" as a link to change "Have you ever been diagnosed with cancer?" under "Your health"
    When I click the link to change "Have you ever been diagnosed with cancer?" under "Your health"
    Then I am on "/cancer-diagnosis?change=True"
    And I see "No" selected
    When I fill in and submit my cancer diagnosis with "Yes"
    Then I am on "/check-your-answers"
    And I see "Yes" as a response to "Have you ever been diagnosed with cancer?" under "Your health"
