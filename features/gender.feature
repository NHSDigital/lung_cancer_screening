@Gender
Feature: Gender page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/gender"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/gender"
    And I click "Continue"
    Then I am on "/gender"
    And I see a form error "Select the option that best describes your gender"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/gender"
    Then I see a back link to "/sex-at-birth"
    When I fill in and submit my gender with "Female"
    Then I am on "/ethnicity"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/gender"
    And I fill in and submit my gender with "Female"
    When I go to "/check-your-answers"
    Then I see "Female" as a response to "Gender identity" under "About you"
    And I see "/gender?change=True" as a link to change "Gender identity" under "About you"
    When I click the link to change "Gender identity" under "About you"
    Then I am on "/gender?change=True"
    And I see "Female" selected
    When I fill in and submit my gender with "Female"
    Then I am on "/check-your-answers"
    And I see "Female" as a response to "Gender identity" under "About you"

