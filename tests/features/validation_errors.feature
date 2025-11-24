Feature: Validation errors
  Scenario: Date of birth form errors
    Given I have started the questionnaire
    When I go to "/date-of-birth"
    And I submit the form
    Then I am on "/date-of-birth"
    And I see a form error "Enter your date of birth"
    When I fill in and submit my date of birth with "51-01-2001"
    Then I am on "/date-of-birth"
    And I see a form error "Date of birth must be a real date"
    When I fill in and submit my date of birth with "01-13-2001"
    Then I am on "/date-of-birth"
    And I see a form error "Date of birth must be a real date"
    When I fill in and submit my date of birth with "31-02-2001"
    Then I am on "/date-of-birth"
    And I see a form error "Date of birth must be a real date"

  Scenario: Height form errors
    Given I have started the questionnaire
    When I go to "/height"
    And I submit the form
    Then I am on "/height"
    And I see a form error "Enter your height"
    When I fill in and submit my height with "139.6"
    Then I am on "/height"
    And I see a form error "Height must be between 139.7cm and 243.8 cm"
    When I fill in and submit my height with "243.9"
    Then I am on "/height"
    And I see a form error "Height must be between 139.7cm and 243.8 cm"

  Scenario: Height imperial form errors
    Given I have started the questionnaire
    When I go to "/height?unit=imperial"
    And I submit the form
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

  Scenario: Weight form errors
    Given I have started the questionnaire
    When I go to "/weight"
    And I submit the form
    Then I am on "/weight"
    And I see a form error "Enter your weight"
    When I fill in and submit my weight with "25.3"
    Then I am on "/weight"
    And I see a form error "Weight must be between 25.4kg and 317.5kg"
    When I fill in and submit my weight with "317.6"
    Then I am on "/weight"
    And I see a form error "Weight must be between 25.4kg and 317.5kg"

  Scenario: Weight imperial form errors
    Given I have started the questionnaire
    When I go to "/weight?unit=imperial"
    And I submit the form
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

  Scenario: Sex at birth form errors
    Given I have started the questionnaire
    When I go to "/sex-at-birth"
    And I submit the form
    Then I am on "/sex-at-birth"
    And I see a form error "Select your sex at birth"

  Scenario: Gender form errors
    Given I have started the questionnaire
    When I go to "/gender"
    And I submit the form
    Then I am on "/gender"
    And I see a form error "Select the option that best describes your gender"

  Scenario: Ethnicity form errors
    Given I have started the questionnaire
    When I go to "/ethnicity"
    And I submit the form
    Then I am on "/ethnicity"
    And I see a form error "Select your ethnic background"

  Scenario: Respiratory conditions form errors
    Given I have started the questionnaire
    When I go to "/respiratory-conditions"
    And I submit the form
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions"
    When I fill in and submit my respiratory conditions with "Bronchitis" and "No, I have not had any of these respiratory conditions"
    Then I am on "/respiratory-conditions"
    And I see a form error "Select if you have had any respiratory conditions, or select 'No, I have not had any of these respiratory conditions'"
