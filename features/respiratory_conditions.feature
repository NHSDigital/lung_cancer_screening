Feature: Respiratory conditions page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/respiratory-conditions"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/respiratory-conditions"
    And I click "Continue"
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions"
    When I fill in and submit my respiratory conditions with "Bronchitis" and "No, I have not had any of these respiratory conditions"
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions, or select 'No, I have not had any of these respiratory conditions'"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/respiratory-conditions"
    Then I see a back link to "/education"
    When I fill in and submit my respiratory conditions with "Pneumonia" and "Emphysema"
    Then I am on "/asbestos-exposure"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/respiratory-conditions"
    And I fill in and submit my respiratory conditions with "Pneumonia" and "Emphysema"
    When I go to "/check-your-answers"
    Then I see "Pneumonia and Emphysema" as a response to "Diagnosed respiratory conditions" under "Your health"
    And I see "/respiratory-conditions?change=True" as a link to change "Diagnosed respiratory conditions" under "Your health"
    When I click the link to change "Diagnosed respiratory conditions" under "Your health"
    Then I am on "/respiratory-conditions?change=True"
    When I fill in and submit my respiratory conditions with "Bronchitis" and "Tuberculosis (TB)"
    Then I am on "/check-your-answers"
    And I see "Pneumonia, Emphysema, Bronchitis, and Tuberculosis (TB)" as a response to "Diagnosed respiratory conditions" under "Your health"

