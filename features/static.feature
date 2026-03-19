@StaticContent
Feature: Static Pages
  Scenario: The static pages are available without logging in
    When I go to "/cookies"
    Then I see a phase header "Pilot"
    And I see a link named "feedback"
    And I see a page title "NHS check if you need a lung scan cookies policy"
    And I see a page title tag "NHS check if you need a lung scan cookies - NHS"
    When I go to "/privacy-policy"
    Then I see a phase header "Pilot"
    And I see a link named "feedback"
    And I see a page title "NHS check if you need a lung scan privacy policy"
    And I see a page title tag "NHS check if you need a lung scan privacy policy - NHS"
    When I go to "/contact-us"
    Then I see a page title "Contact us"
    when I go to "/terms-of-use"
    Then I see a page title "NHS check if you need a lung scan terms of use"
    Then I see a page title tag "NHS check if you need a lung scan terms of use - NHS"

  Scenario: The static pages are available when logged in and accessible
    Given I am logged in
    When I go to "/cookies"
    Then I see a phase header "Pilot"
    And I see a link named "feedback"
    And I see a page title tag "NHS check if you need a lung scan cookies - NHS"
    And there are no accessibility violations
    And I see a page title "NHS check if you need a lung scan cookies policy"
    When I go to "/privacy-policy"
    Then I see a phase header "Pilot"
    And I see a link named "feedback"
    And there are no accessibility violations
    And I see a page title "NHS check if you need a lung scan privacy policy"
    And I see a page title tag "NHS check if you need a lung scan privacy policy - NHS"
    When I go to "/contact-us"
    Then there are no accessibility violations
    And I see a page title "Contact us"
    When I go to "/terms-of-use"
    Then I see a page title "NHS check if you need a lung scan terms of use"
    Then I see a page title tag "NHS check if you need a lung scan terms of use - NHS"
