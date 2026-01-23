@SexAtBirth
Feature: Sex at birth page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/sex-at-birth"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/sex-at-birth"
    And I click "Continue"
    Then I am on "/sex-at-birth"
    And I see a form error "Select your sex at birth"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/sex-at-birth"
    Then I see a back link to "/weight"
    When I fill in and submit my sex at birth with "Male"
    Then I am on "/gender"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/sex-at-birth"
    And I fill in and submit my sex at birth with "Male"
    When I go to "/check-your-answers"
    Then I see "Male" as a response to "Sex at birth" under "About you"
    And I see "/sex-at-birth?change=True" as a link to change "Sex at birth" under "About you"
    When I click the link to change "Sex at birth" under "About you"
    Then I am on "/sex-at-birth?change=True"
    And I see "Male" selected
    When I fill in and submit my sex at birth with "Female"
    Then I am on "/check-your-answers"
    And I see "Female" as a response to "Sex at birth" under "About you"

