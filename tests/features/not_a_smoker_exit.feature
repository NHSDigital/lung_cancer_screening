Feature: Non smokers
  Scenario: Non smokers are not elligible
    Given I am logged in
    And I have started the questionnaire
    When I go to "/have-you-ever-smoked"
    And I fill in and submit my smoking status with "No, I have never smoked"
    Then I am on "/non-smoker-exit"
    And I see a title "You do not need an NHS lung health check"
