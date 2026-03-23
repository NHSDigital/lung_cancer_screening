@StaticContent
Feature: Static Pages
  Scenario: The static pages are available without logging in
    When I go to "/start"
    And I click "Accessibility statement"
    Then I am on "/accessibility-statement"
    And I see a page title "Accessibility statement for NHS check if you need a lung scan"
    And I see a phase header "Pilot"
    And I see a link named "feedback"
    When I click "Cookies"
    Then I am on "/cookies"
    And I see a page title "NHS check if you need a lung scan cookies policy"
    When I click "Privacy policy"
    Then I am on "/privacy-policy"
    And I see a page title "NHS check if you need a lung scan privacy policy"
    When I click "Contact us"
    Then I am on "/contact-us"
    And I see a page title "Contact us"
    When I click "Terms of use"
    Then I am on "/terms-of-use"
    And I see a page title "NHS check if you need a lung scan terms of use"

  Scenario: The static pages are available when logged in and accessible
    Given I am logged in
    When I go to "/accessibility-statement"
    Then I see a page title "Accessibility statement for NHS check if you need a lung scan"
    And there are no accessibility violations
    When I go to "/cookies"
    Then I see a page title "NHS check if you need a lung scan cookies policy"
    And there are no accessibility violations
    When I go to "/privacy-policy"
    Then I see a page title "NHS check if you need a lung scan privacy policy"
    And there are no accessibility violations
    When I go to "/contact-us"
    Then I see a page title "Contact us"
    And there are no accessibility violations
    When I go to "/terms-of-use"
    Then I see a page title "NHS check if you need a lung scan terms of use"
    And there are no accessibility violations
