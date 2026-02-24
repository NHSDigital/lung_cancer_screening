@wip
Feature: Smoking history pages
  Scenario: Singular smoking histories
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "30" years
    When I go to "/types-tobacco-smoking"
    And I check "Cigarettes"
    And I check "Cigarettes"
    And I submit the form

    Then I am on "/cigarettes-smoking-current"
    When I check "Yes"
    And I submit the form

    Then I am on "/cigarettes-smoked-total-years"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "15"
    And I submit the form

    Then I am on "/cigarettes-smoking-frequency"
    When I check "Daily"
    And I submit the form

    Then I am on "/cigarettes-smoked-amount"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "10"
    And I submit the form

    Then I am on "/cigarettes-smoking-change"
    When I check "Yes, I used to smoke more than 10 cigarettes a day"
    And I check "Yes, I used to smoke fewer than 10 cigarettes a day"
    And I submit the form

    Then I am on "/cigarettes-smoking-increased-frequency"
    When I check "Weekly"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-amount"
    When I fill in "When you smoked more than 10 cigarettes a day, roughly how many cigarettes did you normally smoke a week?" with "200"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-years"

    When I go to "/check-your-answers"
    Then I see "15 years" as a response to "Total number of years you smoked cigarettes" under "Cigarette smoking history"
    And I see "10 cigarettes a day" as a response to "Current cigarette smoking" under "Cigarette smoking history"
    And I see "200 cigarettes a week" as a response to "When you smoked more than 10 cigarettes a day" under "Cigarette smoking history"

    When I click the link to change "Cigarette" smoking history

    Then I am on "/cigarettes-smoking-current?change=True"
    When I check "Yes"
    And I submit the form

    Then I am on "/cigarettes-smoked-total-years?change=True"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "17"
    And I submit the form

    Then I am on "/cigarettes-smoking-frequency?change=True"
    When I check "Monthly"
    And I submit the form

    Then I am on "/cigarettes-smoked-amount?change=True"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal month?" with "25"
    And I submit the form

    Then I am on "/cigarettes-smoking-change?change=True"
    When I check "Yes, I used to smoke more than 25 cigarettes a month"
    And I check "Yes, I used to smoke fewer than 25 cigarettes a month"
    And I submit the form

    Then I am on "/cigarettes-smoking-increased-frequency?change=True"
    When I check "Daily"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-amount?change=True"
    When I fill in "When you smoked more than 25 cigarettes a month, roughly how many cigarettes did you normally smoke a day?" with "40"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-years?change=True"

    When I go to "/check-your-answers"
    Then I see "17 years" as a response to "Total number of years you smoked cigarettes" under "Cigarette smoking history"
    And I see "25 cigarettes a month" as a response to "Current cigarette smoking" under "Cigarette smoking history"
    And I see "40 cigarettes a day" as a response to "When you smoked more than 25 cigarettes a month" under "Cigarette smoking history"
