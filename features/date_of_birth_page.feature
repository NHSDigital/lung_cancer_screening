Feature: Date of birth page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/date-of-birth"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have started the questionnaire
    When I go to "/date-of-birth"
    When I click "Continue"
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
    And there are no accessibility violations

  Scenario: Eligibility of people not in age range
    Given I am logged in
    When I go to "/date-of-birth"
    And I fill in and submit my date of birth with "01-01-1900"
    Then I am on "/age-range-exit"
    And I see a title "You are not eligible for lung cancer screening"

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/date-of-birth"
    Then I see a back link to "/have-you-ever-smoked"
    When I fill in and submit my date of birth as 55 years ago
    Then I am on "/check-if-you-need-an-appointment"

  Scenario: Checking responses and changing them
    Given I am logged in
    When I go to "/date-of-birth"
    And I fill in and submit my date of birth as 55 years ago
    When I go to "/check-your-answers"
    Then I see a date 55 years ago as a response to "Date of birth" under "Eligibility"
    And I see "/date-of-birth?change=True" as a link to change "Date of birth" under "Eligibility"
    When I click the link to change "Date of birth" under "Eligibility"
    Then I am on "/date-of-birth?change=True"
    When I fill in and submit my date of birth as 60 years ago
    Then I am on "/check-your-answers"
    And I see a date 60 years ago as a response to "Date of birth" under "Eligibility"
