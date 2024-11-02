Feature: Update the description of an existing todo item
  As a user, I want to update the description of an existing todo item so that I can provide more details about the task.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects
    And a todo item with title "Buy groceries" exists

  Scenario: Successfully update the description of an existing todo item
    When I update the description of the todo item with title "Buy groceries" to "Milk, Eggs, Bread"
    Then the todo item should have description "Milk, Eggs, Bread"

  Scenario: Update the description and title of an existing todo item
    When I update the title of the todo item with title "Buy groceries" to "Go shopping" and description to "At the supermarket"
    Then the todo item should have title "Go shopping" and description "At the supermarket"

  Scenario: Fail to update the description of a non-existent todo item
    When I attempt to update the description of a todo item with id "9999" to "This should fail"
    Then I should receive an error message indicating the todo item does not exist
