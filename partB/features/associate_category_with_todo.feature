Feature: Associate a category with a todo item
  As a user, I want to associate a category with a todo item so that I can organize my tasks into categories.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects
    And a todo item with title "Buy groceries" exists
    And a category with title "Errands" exists

  Scenario: Successfully associate an existing category with an existing todo item
    When I associate the category "Errands" with the todo item "Buy groceries"
    Then the todo item "Buy groceries" should be associated with the category "Errands"

  Scenario: Create a new category and associate it with an existing todo item
    When I create a category with title "Chores" and associate it with the todo item "Buy groceries"
    Then the todo item "Buy groceries" should be associated with the category "Chores"

  Scenario: Fail to associate a non-existent category with a todo item
    When I attempt to associate a non-existent category with id "9999" with the todo item "Buy groceries"
    Then I should receive an error message indicating the category does not exist
