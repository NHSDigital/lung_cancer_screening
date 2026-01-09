Feature: Have you ever smoked page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/have-you-ever-smoked"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/have-you-ever-smoked"
    And I submit the form
    Then I am on "/have-you-ever-smoked"
    And I see a form error "Select if you have ever smoked"
    And there are no accessibility violations

  Scenario: Eligibility of non smokers
    Given I am logged in
    When I go to "/have-you-ever-smoked"
    And I fill in and submit my smoking status with "No, I have never smoked"
    Then I am on "/non-smoker-exit"
    And I see a title "You are not eligible for lung cancer screening"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/have-you-ever-smoked"
    Then I see a back link to "/start"
    When I fill in and submit my smoking status with "Yes, I used to smoke"
    Then I am on "/date-of-birth"
