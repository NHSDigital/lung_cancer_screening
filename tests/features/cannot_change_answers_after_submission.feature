Feature: Participants with submitted responses
  Scenario: Cannot change responses once submitted
    Given I am logged in
    And I have already submitted my responses
    When I go to "/start"
    And I click "Start"
    Then I am on "/start"
