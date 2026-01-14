@AsbestosExposure
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

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/asbestos-exposure"
    And I fill in and submit my asbestos exposure with "No"
    When I go to "/check-your-answers"
    Then I see "No" as a response to "Have you ever worked in a job where you were exposed to asbestos?" under "Your health"
    And I see "/asbestos-exposure?change=True" as a link to change "Have you ever worked in a job where you were exposed to asbestos?" under "Your health"
    When I click the link to change "Have you ever worked in a job where you were exposed to asbestos?" under "Your health"
    Then I am on "/asbestos-exposure?change=True"
    And I see "No" selected
    When I fill in and submit my asbestos exposure with "Yes"
    Then I am on "/check-your-answers"
    And I see "Yes" as a response to "Have you ever worked in a job where you were exposed to asbestos?" under "Your health"
