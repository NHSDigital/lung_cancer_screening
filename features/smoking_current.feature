@SmokingHistory
@SmokingCurrent
Feature: Smoking current page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/cigarettes-smoking-current"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/cigarettes-smoking-current"
    And I click "Continue"
    Then I am on "/cigarettes-smoking-current"
    And I see a form error "Select if you currently smoke cigarettes"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    And I have answered questions showing I have smoked "Cigarettes"
    When I go to "/cigarettes-smoking-current"
    Then I see a back link to "/types-tobacco-smoking"
    When I check "Yes" and submit
    Then I am on "/cigarettes-smoked-total-years"
