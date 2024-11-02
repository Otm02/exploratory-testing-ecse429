Feature: Associate a project with a todo item
  As a user, I want to associate a project with a todo item so that I can organize my tasks into projects.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects
    And a todo item with title "Buy groceries" exists
    And a project with title "Shopping" exists

  Scenario: Successfully associate an existing project with an existing todo item
    When I associate the project "Shopping" with the todo item "Buy groceries"
    Then the todo item "Buy groceries" should be associated with the project "Shopping"

  Scenario: Create a new project and associate it with an existing todo item
    When I create a project with title "Errands" and associate it with the todo item "Buy groceries"
    Then the todo item "Buy groceries" should be associated with the project "Errands"

  Scenario: Fail to associate a non-existent project with a todo item
    When I attempt to associate a non-existent project with id "9999" with the todo item "Buy groceries"
    Then I should receive an error message indicating the project does not exist
