@AgeWhenStartedSmoking
Feature: Questionnaire
  Scenario: Cannot change responses once submitted
    Given I am logged in
    And I have recently submitted my responses
    When I go to "/start"
    And I click "Start now"
    Then I am on "/confirmation"

  Scenario: The user can complete the full questionnaire
    Given I am logged in
    When I go to "/start"
    And I click "Start now"

    Then I am on "/have-you-ever-smoked"
    When I fill in and submit my smoking status with "Yes, I used to smoke"

    Then I am on "/date-of-birth"
    When I fill in and submit my date of birth as 55 years ago

    Then I am on "/check-if-you-need-an-appointment"
    When I check "No, I can continue online" and submit

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
    When I fill in and submit my education with "A-levels"

    Then I am on "/respiratory-conditions"
    When I fill in and submit my respiratory conditions with "Pneumonia" and "Emphysema"

    Then I am on "/asbestos-exposure"
    When I fill in and submit my asbestos exposure with "No"

    Then I am on "/cancer-diagnosis"
    When I fill in and submit my cancer diagnosis with "No"

    Then I am on "/family-history-lung-cancer"
    When I fill in and submit my family history lung cancer with "Yes"

    Then I am on "/relatives-age-when-diagnosed"
    When I fill in and submit my relatives age when diagnosed with "Yes, they were younger than 60"

    Then I am on "/age-when-started-smoking"
    When I fill in "How old were you when you started smoking?" as "18" and submit

    Then I am on "/check-your-answers"
    And I see a back link to "/age-when-started-smoking"

    And I see "Yes, I used to smoke" as a response to "Have you ever smoked tobacco?" under "Eligibility"
    And I see a date 55 years ago as a response to "Date of birth" under "Eligibility"

    And I see "5 feet 7 inches" as a response to "Height" under "About you"
    And I see "5 stone 10 pounds" as a response to "Weight" under "About you"
    And I see "Male" as a response to "Sex at birth" under "About you"
    And I see "Female" as a response to "Gender identity" under "About you"
    And I see "White" as a response to "Ethnic background" under "About you"

    And I see "Pneumonia and Emphysema" as a response to "Diagnosed respiratory conditions" under "Your health"
    And I see "No" as a response to "Have you ever worked in a job where you were exposed to asbestos?" under "Your health"
    And I see "No" as a response to "Have you ever been diagnosed with cancer?" under "Your health"

    And I see "Yes" as a response to "Have any of your parents, siblings or children ever been diagnosed with lung cancer?" under "Family history"
    And I see "Yes, they were younger than 60" as a response to "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?" under "Family history"

    When I click "Submit"
    Then I am on "/confirmation"
