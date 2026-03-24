@Confirmation
Feature: Confirmation
  Scenario: Confirmation page has no accessibility violations
    Given I am logged in
    And I have recently submitted my responses
    When I go to "/start"
    And I click "Continue"
    Then I am on "/confirmation"
    And there are no accessibility violations
