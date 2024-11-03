Feature: Associate a category with a todo item
  As a user, I want to associate a category with a todo item so that I can organize my tasks into categories.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully associate an existing category with an existing todo item
    Given a todo item with title "<todo_title>" exists
    And a category with title "<category_title>" exists
    When I associate the category "<category_title>" with the todo item "<todo_title>"
    Then the todo item "<todo_title>" should be associated with the category "<category_title>"

    Examples:
      | todo_title    | category_title |
      | Buy groceries | Errands        |
      | Clean house   | Chores         |
      | Finish report | Work           |

  Scenario Outline: Create a new category and associate it with an existing todo item
    Given a todo item with title "<todo_title>" exists
    When I create a category with title "<new_category_title>" and associate it with the todo item "<todo_title>"
    Then the todo item "<todo_title>" should be associated with the category "<new_category_title>"

    Examples:
      | todo_title    | new_category_title |
      | Buy groceries | Personal           |
      | Clean house   | Home               |
      | Finish report | Office             |

  Scenario Outline: Fail to associate a non-existent category with a todo item
    Given a todo item with title "<todo_title>" exists
    When I attempt to associate a non-existent category with id "<invalid_category_id>" with the todo item "<todo_title>"
    Then I should receive an error message indicating the category does not exist

    Examples:
      | todo_title    | invalid_category_id |
      | Buy groceries |                9999 |
      | Clean house   |                8888 |
      | Finish report |                7777 |
