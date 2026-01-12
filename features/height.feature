Feature: Height page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/height"
    Then there are no accessibility violations
    When I click "Switch to feet and inches"
    Then there are no accessibility violations

  Scenario: Metric form errors
    Given I am logged in
    When I go to "/height"
    And I click "Continue"
    Then I am on "/height"
    And I see a form error "Enter your height"
    When I fill in and submit my height with "139.6"
    Then I am on "/height"
    And I see a form error "Height must be between 139.7cm and 243.8 cm"
    When I fill in and submit my height with "243.9"
    Then I am on "/height"
    And I see a form error "Height must be between 139.7cm and 243.8 cm"
    And there are no accessibility violations

  Scenario: Imperial form errors
    Given I am logged in
    When I go to "/height?unit=imperial"
    And I click "Continue"
    Then I am on "/height?unit=imperial"
    And I see a form error "Enter your height"
    When I fill in and submit my height with "5.2" feet and "2" inches
    Then I am on "/height?unit=imperial"
    And I see a form error "Feet must be in whole numbers"
    When I fill in and submit my height with "5" feet and "2.2" inches
    Then I am on "/height?unit=imperial"
    And I see a form error "Inches must be in whole numbers"
    When I fill in and submit my height with "8" feet and "1" inch
    Then I am on "/height?unit=imperial"
    And I see a form error "Height must be between 4 feet 7 inches and 8 feet"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/height"
    Then I see a back link to "/check-if-you-need-an-appointment"
    When I fill in and submit my height with "170"
    Then I am on "/weight"
    When I click "Back"
    And I click "Switch to feet and inches"
    When I fill in and submit my height with "5" feet and "7" inches
    Then I am on "/weight"
    When I click "Back"
    Then I am on "/height"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/height"
    And I fill in and submit my height with "170"
    When I go to "/check-your-answers"
    Then I see "170 cm" as a response to "Height" under "About you"
    And I see "/height?change=True" as a link to change "Height" under "About you"
    When I click the link to change "Height" under "About you"
    Then I am on "/height?change=True"
    When I click "Switch to feet and inches"
    And I fill in and submit my height with "5" feet and "7" inches
    Then I am on "/check-your-answers"
    And I see "5 feet 7 inches" as a response to "Height" under "About you"

