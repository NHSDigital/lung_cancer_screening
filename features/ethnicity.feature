@Ethnicity
Feature: Ethnicity page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/ethnicity"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/ethnicity"
    And I click "Continue"
    Then I am on "/ethnicity"
    And I see a form error "Select your ethnic background"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/ethnicity"
    Then I see a back link to "/gender"
    When I fill in and submit my ethnicity with "White"
    Then I am on "/education"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/ethnicity"
    And I fill in and submit my ethnicity with "White"
    When I go to "/check-your-answers"
    Then I see "White" as a response to "Ethnic background" under "About you"
    And I see "/ethnicity?change=True" as a link to change "Ethnic background" under "About you"
    When I click the link to change "Ethnic background" under "About you"
    Then I am on "/ethnicity?change=True"
    And I see "White" selected
    When I fill in and submit my ethnicity with "Black, African, Caribbean or Black British"
    Then I am on "/check-your-answers"
    And I see "Black, African, Caribbean or Black British" as a response to "Ethnic background" under "About you"

