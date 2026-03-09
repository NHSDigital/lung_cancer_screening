@Cookies
Feature: Cookies page
  Scenario: The page is accessible
    Given I am logged in
    When I go to "/cookies"
    Then there are no accessibility violations
