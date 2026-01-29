@PeriodsWhenYouStoppedSmoking
Feature: Periods when you stopped smoking page
  Scenario: The page is accessible
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/periods-when-you-stopped-smoking"
    # TODO: problem with aria expanded from nhsuk frontend
    # Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    When I go to "/periods-when-you-stopped-smoking"
    When I submit the form
    Then I am on "/periods-when-you-stopped-smoking"
    And I see a form error "Select if you ever stopped smoking for periods of 1 year or longer"
    # TODO: problem with aria expanded from nhsuk frontend
    # And there are no accessibility violations

  Scenario: Navigating backwards and forwards
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/periods-when-you-stopped-smoking"
    Then I see a back link to "/age-when-started-smoking"
    When I check "Yes"
    And I fill in "Enter the total number of years you stopped smoking for" with "1"
    And I submit the form
    Then I am on "/types-tobacco-smoking"

  Scenario: Checking responses and changing them
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "10" years
    When I go to "/periods-when-you-stopped-smoking"
    And I check "Yes"
    And I fill in "Enter the total number of years you stopped smoking for" with "1"
    And I submit the form
    When I go to "/check-your-answers"
    Then I see "Yes (1 years)" as a response to "Have you ever stopped smoking for periods of 1 year or longer?" under "Smoking history"
    And I see "/periods-when-you-stopped-smoking?change=True" as a link to change "Have you ever stopped smoking for periods of 1 year or longer?" under "Smoking history"
    When I click the link to change "Have you ever stopped smoking for periods of 1 year or longer?" under "Smoking history"
    Then I am on "/periods-when-you-stopped-smoking?change=True"
    And I see "Yes" selected
    When I check "No"
    And I submit the form
    Then I am on "/check-your-answers"
    And I see "No" as a response to "Have you ever stopped smoking for periods of 1 year or longer?" under "Smoking history"
