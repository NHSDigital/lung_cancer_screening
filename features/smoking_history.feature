@SmokingHistory
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
    When I fill in "Roughly how many years did you smoke 200 cigarettes a week?" with "5"
    And I submit the form

    Then I am on "/cigarettes-smoking-decreased-frequency"
    When I check "Monthly"
    And I submit the form

    Then I am on "/cigarettes-smoked-decreased-amount"
    When I fill in "When you smoked fewer than 10 cigarettes a day, roughly how many cigarettes did you normally smoke a month?" with "1"
    And I submit the form

    Then I am on "/cigarettes-smoked-decreased-years"
    When I fill in "Roughly how many years did you smoke 1 cigarettes a month?" with "2"
    And I submit the form

    Then I am on "/check-your-answers"
    Then I see "15 years" as a response to "Total number of years you smoked cigarettes" under "Cigarette smoking history"
    And I see "10 cigarettes a day" as a response to "Current cigarette smoking" under "Cigarette smoking history"
    And I see "200 cigarettes a week for 5 years" as a response to "When you smoked more than 10 cigarettes a day" under "Cigarette smoking history"
    And I see "1 cigarettes a month for 2 years" as a response to "When you smoked fewer than 10 cigarettes a day" under "Cigarette smoking history"

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

    And I see "40 cigarettes a day for 5 years" as a response to "When you smoked more than 25 cigarettes a month" under "Cigarette smoking history"

  @wip
  Scenario: Multiple smoking histories
    Given I am logged in
    And I have answered questions showing I am eligible
    And I have answered questions showing I have smoked for "30" years
    When I go to "/types-tobacco-smoking"
    And I check "Cigarettes"
    And I check "Rolling tobacco"
    And I check "Pipe"
    And I check "Cigarillos"
    And I check "Small cigars"
    And I check "Medium cigars"
    And I submit the form

  # Cigarettes with increased and decreased
    Then I am on "/cigarettes-smoking-current"
    And I see a page title "Do you currently smoke cigarettes?"
    When I check "Yes"
    And I submit the form

    Then I am on "/cigarettes-smoked-total-years"
    When I fill in "Roughly how many years have you smoked cigarettes?" with "15"
    And I submit the form

    Then I am on "/cigarettes-smoking-frequency"
    And I see a page title "How often do you smoke cigarettes?"
    When I check "Daily"
    And I submit the form

    Then I am on "/cigarettes-smoked-amount"
    When I fill in "Roughly how many cigarettes do you currently smoke in a normal day?" with "10"
    And I submit the form

    Then I am on "/cigarettes-smoking-change"
    And I see a page title "Has the number of cigarettes you normally smoke changed over time?"
    When I check "Yes, I used to smoke more than 10 cigarettes a day"
    And I check "Yes, I used to smoke fewer than 10 cigarettes a day"
    And I submit the form

    Then I am on "/cigarettes-smoking-increased-frequency"
    And I see a page title "When you smoked more than 10 cigarettes a day, how often did you smoke cigarettes?"
    When I check "Weekly"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-amount"
    When I fill in "When you smoked more than 10 cigarettes a day, roughly how many cigarettes did you normally smoke a week?" with "200"
    And I submit the form

    Then I am on "/cigarettes-smoked-increased-years"
    When I fill in "Roughly how many years did you smoke 200 cigarettes a week?" with "5"
    And I submit the form

    Then I am on "/cigarettes-smoking-decreased-frequency"
    And I see a page title "When you smoked fewer than 10 cigarettes a day, how often did you smoke cigarettes?"
    When I check "Monthly"
    And I submit the form

    Then I am on "/cigarettes-smoked-decreased-amount"
    When I fill in "When you smoked fewer than 10 cigarettes a day, roughly how many cigarettes did you normally smoke a month?" with "1"
    And I submit the form

    Then I am on "/cigarettes-smoked-decreased-years"
    When I fill in "Roughly how many years did you smoke 1 cigarettes a month?" with "2"
    And I submit the form

  # Rolling tobacco with increased and decreased
    Then I am on "/rolling-tobacco-smoking-current"
    And I see a page title "Do you currently smoke rolling tobacco?"
    When I check "Yes"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-total-years"
    When I fill in "Roughly how many years have you smoked rolling tobacco?" with "26"
    And I submit the form

    Then I am on "/rolling-tobacco-smoking-frequency"
    And I see a page title "How often do you smoke rolling tobacco?"
    When I check "Weekly"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-amount"
    When I fill in "Roughly how many grams of rolling tobacco do you currently smoke in a normal week?" with "25"
    And I submit the form

    Then I am on "/rolling-tobacco-smoking-change"
    When I check "Yes, I used to smoke more than 25 grams of rolling tobacco a week"
    And I check "Yes, I used to smoke fewer than 25 grams of rolling tobacco a week"
    And I submit the form

    Then I am on "/rolling-tobacco-smoking-increased-frequency"
    And I see a page title "When you smoked more than 25 grams of rolling tobacco a week, how often did you smoke rolling tobacco?"
    When I check "Daily"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-increased-amount"
    When I fill in "When you smoked more than 25 grams of rolling tobacco a week, roughly how many grams of rolling tobacco did you normally smoke a day?" with "12"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-increased-years"
    When I fill in "Roughly how many years did you smoke 12 grams of rolling tobacco a day?" with "10"
    And I submit the form

    Then I am on "/rolling-tobacco-smoking-decreased-frequency"
    When I check "Monthly"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-decreased-amount"
    When I fill in "When you smoked fewer than 25 grams of rolling tobacco a week, roughly how many grams of rolling tobacco did you normally smoke a month?" with "5"
    And I submit the form

    Then I am on "/rolling-tobacco-smoked-decreased-years"
    When I fill in "Roughly how many years did you smoke 5 grams of rolling tobacco a month?" with "4"
    And I submit the form

  # Pipe with increased and decreased
    Then I am on "/pipe-smoking-current"
    And I see a page title "Do you currently smoke a pipe?"
    When I check "Yes"
    And I submit the form

    Then I am on "/pipe-smoked-total-years"
    When I fill in "Roughly how many years have you smoked a pipe?" with "26"
    And I submit the form

    Then I am on "/pipe-smoking-frequency"
    And I see a page title "How often do you smoke a pipe?"
    When I check "Weekly"
    And I submit the form

    Then I am on "/pipe-smoked-amount"
    When I fill in "Roughly how many full pipe loads do you currently smoke in a normal week?" with "25"
    And I submit the form

    Then I am on "/pipe-smoking-change"
    And I see a page title "Has the number of full pipe loads you normally smoke changed over time?"
    When I check "Yes, I used to smoke more than 25 full pipe loads a week"
    And I check "Yes, I used to smoke fewer than 25 full pipe loads a week"
    And I submit the form

    Then I am on "/pipe-smoking-increased-frequency"
    And I see a page title "When you smoked more than 25 full pipe loads a week, how often did you smoke a pipe?"
    When I check "Daily"
    And I submit the form

    Then I am on "/pipe-smoked-increased-amount"
    When I fill in "When you smoked more than 25 full pipe loads a week, roughly how many full pipe loads did you normally smoke a day?" with "12"
    And I submit the form

    Then I am on "/pipe-smoked-increased-years"
    When I fill in "Roughly how many years did you smoke 12 full pipe loads a day?" with "10"
    And I submit the form

    Then I am on "/pipe-smoking-decreased-frequency"
    When I check "Monthly"
    And I submit the form

    Then I am on "/pipe-smoked-decreased-amount"
    When I fill in "When you smoked fewer than 25 full pipe loads a week, roughly how many full pipe loads did you normally smoke a month?" with "5"
    And I submit the form

    Then I am on "/pipe-smoked-decreased-years"
    When I fill in "Roughly how many years did you smoke 5 full pipe loads a month?" with "4"
    And I submit the form

  # Small cigars with no change
    Then I am on "/small-cigars-smoking-current"
    And I see a page title "Do you currently smoke small cigars?"
    When I check "Yes"
    And I submit the form

    Then I am on "/small-cigars-smoked-total-years"
    When I fill in "Roughly how many years have you smoked small cigars?" with "8"
    And I submit the form

    Then I am on "/small-cigars-smoking-frequency"
    And I see a page title "How often do you smoke small cigars?"
    When I check "Monthly"
    And I submit the form

    Then I am on "/small-cigars-smoked-amount"
    When I fill in "Roughly how many small cigars do you currently smoke in a normal month?" with "9"
    And I submit the form

    Then I am on "/small-cigars-smoking-change"
    And I see a page title "Has the number of small cigars you normally smoke changed over time?"
    When I check "No, it has not changed"
    And I submit the form

  # Medium cigars with only decreased
    Then I am on "/medium-cigars-smoking-current"
    And I see a page title "Do you currently smoke medium cigars?"
    When I check "Yes"
    And I submit the form

    Then I am on "/medium-cigars-smoked-total-years"
    When I fill in "Roughly how many years have you smoked medium cigars?" with "8"
    And I submit the form

    Then I am on "/medium-cigars-smoking-frequency"
    And I see a page title "How often do you smoke medium cigars?"
    When I check "Monthly"
    And I submit the form

    Then I am on "/medium-cigars-smoked-amount"
    When I fill in "Roughly how many medium cigars do you currently smoke in a normal month?" with "9"
    And I submit the form

    Then I am on "/medium-cigars-smoking-change"
    And I see a page title "Has the number of medium cigars you normally smoke changed over time?"
    When I check "Yes, I used to smoke fewer than 9 medium cigars a month"
    And I submit the form

    Then I am on "/medium-cigars-smoking-decreased-frequency"
    And I see a page title "When you smoked fewer than 9 medium cigars a month, how often did you smoke medium cigars?"
    When I check "Weekly"
    And I submit the form

    Then I am on "/medium-cigars-smoked-decreased-amount"
    When I fill in "When you smoked fewer than 9 medium cigars a month, roughly how many medium cigars did you normally smoke a week?" with "7"
    And I submit the form

    Then I am on "/medium-cigars-smoked-decreased-years"
    When I fill in "Roughly how many years did you smoke 7 medium cigars a week?" with "3"
    And I submit the form

  # Cigarillos with only increased
    Then I am on "/cigarillos-smoking-current"
    And I see a page title "Do you currently smoke cigarillos?"
    When I check "Yes"
    And I submit the form

    Then I am on "/cigarillos-smoked-total-years"
    When I fill in "Roughly how many years have you smoked cigarillos?" with "4"
    And I submit the form

    Then I am on "/cigarillos-smoking-frequency"
    And I see a page title "How often do you smoke cigarillos?"
    When I check "Monthly"
    And I submit the form

    Then I am on "/cigarillos-smoked-amount"
    When I fill in "Roughly how many cigarillos do you currently smoke in a normal month?" with "2"
    And I submit the form

    Then I am on "/cigarillos-smoking-change"
    And I see a page title "Has the number of cigarillos you normally smoke changed over time?"
    When I check "Yes, I used to smoke more than 2 cigarillos a month"
    And I submit the form

    Then I am on "/cigarillos-smoking-increased-frequency"
    And I see a page title "When you smoked more than 2 cigarillos a month, how often did you smoke cigarillos?"
    When I check "Weekly"
    And I submit the form

    Then I am on "/cigarillos-smoked-increased-amount"
    When I fill in "When you smoked more than 2 cigarillos a month, roughly how many cigarillos did you normally smoke a week?" with "4"
    And I submit the form

    Then I am on "/cigarillos-smoked-increased-years"
    When I fill in "Roughly how many years did you smoke 4 cigarillos a week?" with "3"
    And I submit the form

  # Check your answers
    Then I am on "/check-your-answers"

    Then I see "15 years" as a response to "Total number of years you smoked cigarettes" under "Cigarette smoking history"
    And I see "10 cigarettes a day" as a response to "Current cigarette smoking" under "Cigarette smoking history"
    And I see "200 cigarettes a week for 5 years" as a response to "When you smoked more than 10 cigarettes a day" under "Cigarette smoking history"
    And I see "1 cigarettes a month for 2 years" as a response to "When you smoked fewer than 10 cigarettes a day" under "Cigarette smoking history"

    Then I see "26 years" as a response to "Total number of years you smoked rolling tobacco" under "Rolling tobacco smoking history"
    And I see "25 grams of rolling tobacco a week" as a response to "Current rolling tobacco smoking" under "Rolling tobacco smoking history"
    And I see "12 grams of rolling tobacco a day for 10 years" as a response to "When you smoked more than 25 grams of rolling tobacco a week" under "Rolling tobacco smoking history"
    And I see "5 grams of rolling tobacco a month for 4 years" as a response to "When you smoked fewer than 25 grams of rolling tobacco a week" under "Rolling tobacco smoking history"

    Then I see "26 years" as a response to "Total number of years you smoked a pipe" under "Pipe smoking history"
    And I see "25 full pipe loads a week" as a response to "Current pipe smoking" under "Pipe smoking history"
    And I see "12 full pipe loads a day for 10 years" as a response to "When you smoked more than 25 full pipe loads a week" under "Pipe smoking history"
    And I see "5 full pipe loads a month for 4 years" as a response to "When you smoked fewer than 25 full pipe loads a week" under "Pipe smoking history"

    Then I see "8 years" as a response to "Total number of years you smoked medium cigars" under "Medium cigar smoking history"
    And I see "9 medium cigars a month" as a response to "Current medium cigar smoking" under "Medium cigar smoking history"
    And I see "7 medium cigars a week for 3 years" as a response to "When you smoked fewer than 9 medium cigars a month" under "Medium cigar smoking history"

    Then I see "4 years" as a response to "Total number of years you smoked cigarillos" under "Cigarillo smoking history"
    And I see "2 cigarillos a month" as a response to "Current cigarillo smoking" under "Cigarillo smoking history"
    And I see "4 cigarillos a week for 3 years" as a response to "When you smoked more than 2 cigarillos a month" under "Cigarillo smoking history"

  # Change cigarette smoking history with increased and decreased
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
    When I submit the form

    Then I am on "/cigarettes-smoking-decreased-frequency?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoked-decreased-amount?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoked-decreased-years?change=True"
    When I submit the form

    Then I am on "/check-your-answers"
    Then I see "17 years" as a response to "Total number of years you smoked cigarettes" under "Cigarette smoking history"
    And I see "25 cigarettes a month" as a response to "Current cigarette smoking" under "Cigarette smoking history"

    And I see "40 cigarettes a day for 5 years" as a response to "When you smoked more than 25 cigarettes a month" under "Cigarette smoking history"

  # Change medium cigars with decreased
    When I click the link to change "Medium cigar" smoking history

    Then I am on "/medium-cigars-smoking-current?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoked-total-years?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoking-frequency?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoked-amount?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoking-change?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoking-decreased-frequency?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoked-decreased-amount?change=True"
    When I submit the form

    Then I am on "/medium-cigars-smoked-decreased-years?change=True"
    When I submit the form

    Then I am on "/check-your-answers"

  # Change cigarillos with increased
    When I click the link to change "Cigarillo" smoking history

    Then I am on "/cigarillos-smoking-current?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoked-total-years?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoking-frequency?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoked-amount?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoking-change?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoking-increased-frequency?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoked-increased-amount?change=True"
    When I submit the form

    Then I am on "/cigarillos-smoked-increased-years?change=True"
    When I submit the form

    Then I am on "/check-your-answers"

  # Change cigarettes change to no change
    When I click the link to change "Cigarette" smoking history

    Then I am on "/cigarettes-smoking-current?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoked-total-years?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoking-frequency?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoked-amount?change=True"
    When I submit the form

    Then I am on "/cigarettes-smoking-change?change=True"
    When I uncheck "Yes, I used to smoke more than 25 cigarettes a month"
    And I uncheck "Yes, I used to smoke fewer than 25 cigarettes a month"
    And I check "No, it has not changed"
    When I submit the form

    Then I am on "/check-your-answers"


