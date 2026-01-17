Feature: Smoke Test
  Scenario: Basic sanity check
    Given the digitalengn repository is initialized
    When I check the project structure
    Then I should see the mbse, docs, and features directories

  Scenario: Verify core infrastructure URLs in Minikube
    Given the infrastructure is launched in Minikube
    When I access the following core URLs:
      | name        | path   |
      | digitalengn | /      |
      | openproject | /plan  |
      | gitlab      | /git   |
    Then I should receive a valid response from each URL
