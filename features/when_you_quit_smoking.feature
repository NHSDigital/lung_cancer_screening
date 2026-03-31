@SmokingHistory
@WhenYouQuitSmoking
Feature: Age quit smoking
  # Scenario: The page is accessible
  #   Given I am logged in
  #   And I have answered questions showing I am eligible
  #   When I go to "/age-when-started-smoking"
  #   Then there are no accessibility violations

  Scenario: Form errors
    Given I am logged in
    And I have answered questions showing I am eligible
    And I am 60 years old
    And I have answered questions showing I started smoking "30" years ago
    When I go to "/when-you-quit-smoking"
    And I click "Continue"
    Then I am on "/when-you-quit-smoking"
    And I see a form error "Enter your age when you quit smoking"
    And there are no accessibility violations

  # Scenario: Navigating backwards and forwards
  #   Given I am logged in
  #   And I have answered questions showing I am eligible
  #   When I go to "/age-when-started-smoking"
  #   Then I see a back link to "/relatives-age-when-diagnosed"
  #   When I fill in "How old were you when you started smoking?" as "18" and submit
  #   Then I am on "/periods-when-you-stopped-smoking"

  # Scenario: Checking responses and changing them
  #   Given I am logged in
  #   And I have answered questions showing I am eligible
  #   When I go to "/age-when-started-smoking"
  #   And I fill in "How old were you when you started smoking?" as "18" and submit
  #   When I go to "/check-your-answers"
  #   Then I see "18" as a response to "Age you started smoking" under "Smoking history"
  #   And I see "/age-when-started-smoking?change=True" as a link to change "Age you started smoking" under "Smoking history"
  #   When I click the link to change "Age you started smoking" under "Smoking History"
  #   Then I am on "/age-when-started-smoking?change=True"
  #   And I see "18" filled in for "How old were you when you started smoking?"
  #   When I fill in "How old were you when you started smoking?" as "22" and submit
  #   Then I am on "/periods-when-you-stopped-smoking?change=True"
