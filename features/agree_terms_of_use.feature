@TermsOfUse
Feature: Check if you need an appointment page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/agree-terms-of-use"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    When I go to "/agree-terms-of-use"
    And I click "Continue"
    Then I am on "/agree-terms-of-use"
    And I see a form error "Agree to the terms of use to continue"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    When I go to "/agree-terms-of-use"
    Then I see a back link to "/start"
    When I check "I agree" and submit
    Then I am on "/have-you-ever-smoked"
