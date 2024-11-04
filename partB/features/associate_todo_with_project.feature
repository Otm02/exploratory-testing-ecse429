Feature: Associate a project with a todo item
  As a user, I want to associate a project with a todo item so that I can organize my tasks into projects.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully associate an existing project with an existing todo item
    Given a todo item with title "<todo_title>" exists
    And a project with title "<project_title>" exists
    When I associate the project "<project_title>" with the todo item "<todo_title>"
    Then the todo item "<todo_title>" should be associated with the project "<project_title>"

    Examples:
      | todo_title    | project_title |
      | Buy groceries | Shopping      |
      | Clean house   | Home          |
      | Finish report | Work          |

  Scenario Outline: Create a new project and associate it with an existing todo item
    Given a todo item with title "<todo_title>" exists
    When I create a project with title "<new_project_title>" and associate it with the todo item "<todo_title>"
    Then the todo item "<todo_title>" should be associated with the project "<new_project_title>"

    Examples:
      | todo_title    | new_project_title |
      | Buy groceries | Errands           |
      | Clean house   | Chores            |
      | Finish report | Office            |

  Scenario Outline: Fail to associate a non-existent project with a todo item
    Given a todo item with title "<todo_title>" exists
    When I attempt to associate a non-existent project with id "<invalid_project_id>" with the todo item "<todo_title>"
    Then I should receive an error message indicating the project does not exist

    Examples:
      | todo_title    | invalid_project_id |
      | Buy groceries |               9999 |
      | Clean house   |               8888 |
      | Finish report |               7777 |
