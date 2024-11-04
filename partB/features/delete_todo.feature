Feature: Delete a todo item
  As a user, I want to delete a todo item so that I can remove irrelevant todos.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully delete an existing todo item
    Given a todo item with title "<todo_title>" exists
    When I delete the todo item with title "<todo_title>"
    Then the todo item "<todo_title>" should no longer exist

    Examples:
      | todo_title    |
      | Old Task      |
      | Buy groceries |
      | Clean house   |

  Scenario Outline: Delete a todo item that is associated with a project and category
    Given a todo item with title "<todo_title>" exists
    And the todo item with title "<todo_title>" is associated with the project "<project_title>" and category "<category_title>"
    When I delete the todo item with title "<todo_title>"
    Then the todo item "<todo_title>" should no longer exist
    And the associations should be removed

    Examples:
      | todo_title    | project_title | category_title |
      | Old Task      | Old Project   | Old Category   |
      | Buy groceries | Shopping      | Errands        |
      | Clean house   | Home          | Chores         |

  Scenario Outline: Fail to delete a non-existent todo item
    When I attempt to delete a todo item with id "<invalid_todo_id>"
    Then I should receive an error message indicating the todo item does not exist

    Examples:
      | invalid_todo_id |
      |            9999 |
      |            8888 |
      |            7777 |
