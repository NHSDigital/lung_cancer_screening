Feature: Participants with submitted responses
  Scenario: Cannot change responses once submitted
    Given a participant abc123 exists
    And the participant abc123 has submitted their responses
    And the participant is on the "/start" path
    When the participant abc123 submits their participant id
    Then the participant should be on the "/start" path
    And the participant should see en error summary "Responses have already been submitted for this participant"
