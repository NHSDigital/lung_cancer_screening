@SmokingHistory
@TypesTobaccoSmoking
Feature: Types tobacco smoking page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/types-tobacco-smoking"
    Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/types-tobacco-smoking"
    And I click "Continue"
    Then I am on "/types-tobacco-smoking"
    And I see a form error "Select the type of tobacco you smoke or have smoked"
    And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/types-tobacco-smoking"
    Then I see a back link to "/periods-when-you-stopped-smoking"
    When I check "Cigarettes"
    And I submit the form
    Then I am on "/cigarettes-smoking-current"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/types-tobacco-smoking"
    And I check "Cigarettes"
    And I check "Cigars"
    And I submit the form
    When I go to "/check-your-answers"
    Then I see "Cigarettes and Cigars" as a response to "Types of tobacco smoked" under "Smoking history"
    And I see "/types-tobacco-smoking?change=True" as a link to change "Types of tobacco smoked" under "Smoking history"
    When I click the link to change "Types of tobacco smoked" under "Smoking history"
    Then I am on "/types-tobacco-smoking?change=True"
    And I see "Cigarettes" selected
    And I see "Cigars" selected
    When I check "Pipe"
    And I click "Continue"
    Then I am on "/cigarettes-smoking-current"
    When I go to "/check-your-answers"
    Then I see "Cigarettes, Pipe, and Cigars" as a response to "Types of tobacco smoked" under "Smoking history"
