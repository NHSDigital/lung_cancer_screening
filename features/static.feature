@StaticContent
Feature: Static Pages
  Scenario: The static pages are accessible
    Given I am logged in
    When I go to "/cookies"
    Then there are no accessibility violations
    When I go to "/privacy-policy"
    Then there are no accessibility violations
