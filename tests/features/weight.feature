Feature: Weight page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/weight"
    Then there are no accessibility violations
    When I click "Switch to stone and pounds"
    Then there are no accessibility violations

  Scenario: Metric form errors
    Given I am logged in
    When I go to "/weight"
    And I click "Continue"
    Then I am on "/weight"
    And I see a form error "Enter your weight"
    When I fill in and submit my weight with "25.3"
    Then I am on "/weight"
    And I see a form error "Weight must be between 25.4kg and 317.5kg"
    When I fill in and submit my weight with "317.6"
    Then I am on "/weight"
    And I see a form error "Weight must be between 25.4kg and 317.5kg"
    And there are no accessibility violations

  Scenario: Imperial form errors
    Given I am logged in
    When I go to "/weight?unit=imperial"
    And I click "Continue"
    Then I am on "/weight?unit=imperial"
    And I see a form error "Enter your weight"
    When I fill in and submit my weight with "5.2" stone and "2" pounds
    Then I am on "/weight?unit=imperial"
    And I see a form error "Stone must be in whole numbers"
    When I fill in and submit my weight with "5" stone and "2.2" pounds
    Then I am on "/weight?unit=imperial"
    And I see a form error "Pounds must be in whole numbers"
    When I fill in and submit my weight with "3" stone and "12" pounds
    Then I am on "/weight?unit=imperial"
    And I see a form error "Weight must be between 4 stone and 50 stone"
    When I fill in and submit my weight with "50" stone and "1" pound
    Then I am on "/weight?unit=imperial"
    And I see a form error "Weight must be between 4 stone and 50 stone"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/weight"
    Then I see a back link to "/height"
    When I fill in and submit my weight with "70"
    Then I am on "/sex-at-birth"
    When I click "Back"
    And I click "Switch to stone and pounds"
    When I fill in and submit my weight with "5" stone and "10" pounds
    Then I am on "/sex-at-birth"
    When I click "Back"
    Then I am on "/weight"

