Feature: Participants with submitted responses
  Scenario: Cannot change responses once submitted
    Given I have already submitted my responses
    When I go to "/start"
    And I submit my participant id
    Then I am on "/start"
    And I should see an error summary "Responses have already been submitted for this participant"
