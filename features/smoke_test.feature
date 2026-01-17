Feature: Smoke Test
  Scenario: Basic sanity check
    Given the digitalengn repository is initialized
    When I check the project structure
    Then I should see the mbse, docs, and features directories
