Feature: Not in age range
  Scenario: Participants outside age range are not elligible
    Given I am logged in
    And I have started the questionnaire
    When I go to "/date-of-birth"
    And I fill in and submit my date of birth with "01-01-1900"
    Then I am on "/age-range-exit"
    And I see a title "You do not need an NHS lung health check"
