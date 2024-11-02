Feature: Delete a todo item
  As a user, I want to delete a todo item so that I can remove irrelevant todos.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects
    And a todo item with title "Old Task" exists

  Scenario: Successfully delete an existing todo item
    When I delete the todo item with title "Old Task"
    Then the todo item "Old Task" should no longer exist

  Scenario: Delete a todo item that is associated with a project and category
    Given the todo item "Old Task" is associated with the project "Old Project" and category "Old Category"
    When I delete the todo item with title "Old Task"
    Then the todo item "Old Task" should no longer exist
    And the associations should be removed

  Scenario: Fail to delete a non-existent todo item
    When I attempt to delete a todo item with id "9999"
    Then I should receive an error message indicating the todo item does not exist
