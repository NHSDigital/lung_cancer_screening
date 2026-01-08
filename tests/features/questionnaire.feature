Feature: Questionnaire
  Scenario: Cannot change responses once submitted
    Given I am logged in
    And I have already submitted my responses
    When I go to "/start"
    And I click "Start"
    Then I am on "/start"

  Scenario: The user can complete the full questionnaire
    Given I am logged in
    When I go to "/start"
    And I click "Start"

    Then I am on "/have-you-ever-smoked"
    When I fill in and submit my smoking status with "Yes, I used to smoke"

    Then I am on "/date-of-birth"
    When I fill in and submit my date of birth as 55 years ago

    Then I am on "/height"
    When I click "Switch to feet and inches"
    And I fill in and submit my height with "5" feet and "7" inches

    Then I am on "/weight"
    When I click "Switch to stone and pounds"
    And I fill in and submit my weight with "5" stone and "10" pounds

    Then I am on "/sex-at-birth"
    When I fill in and submit my sex at birth with "Male"

    Then I am on "/gender"
    When I fill in and submit my gender with "Female"

    Then I am on "/ethnicity"
    When I fill in and submit my ethnicity with "White"

    Then I am on "/education"
    When I click "Continue"

    Then I am on "/respiratory-conditions"
    When I fill in and submit my respiratory conditions with "Pneumonia" and "Emphysema"

    Then I am on "/asbestos-exposure"
    When I fill in and submit my asbestos exposure with "No"

    Then I am on "/cancer-diagnosis"
    When I fill in and submit my cancer diagnosis with "No"

    Then I am on "/family-history-lung-cancer"
    When I fill in and submit my family history lung cancer with "Yes"

    Then I am on "/relatives-age-when-diagnosed"
    And I see a back link to "/family-history-lung-cancer"
    When I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"
    Then I am on "/responses"
    And I see a back link to "/relatives-age-when-diagnosed"
    And I see responses "Have you ever smoked? Yes, I used to smoke"
    And I see responses "What is your date of birth?" with a date 55 years ago
    And I see responses "What is your height? 5 feet 7 inches"
    And I see responses "What is your weight? 5 stone 10 pounds"
    And I see responses "What was your sex at birth? Male"
    And I see responses "Which of these best describes you? Female"
    And I see responses "What is your ethnic background? White"
    And I see responses "Have you ever worked in a job where you might have been exposed to asbestos? No"
    And I see responses "Have you ever been diagnosed with any of the following respiratory conditions? Pneumonia and Emphysema"
    And I see responses "Have you ever been diagnosed with cancer? No"
    And I see responses "Have any of your parents, siblings or children ever been diagnosed with lung cancer Yes"
    And I see responses "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer? Yes, they were younger than 60"
