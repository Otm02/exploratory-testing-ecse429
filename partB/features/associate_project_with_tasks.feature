Feature: Manage Project Tasks
  As a user
  I want to manage tasks within a project
  So that I can organize tasks under specific projects

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully add a task to a project
    Given a project with title "{project_title}" exists
    Given a todo item with title "<todo_title>" exists
    When I add the todo to the project
    Then the project should contain the todo

    Examples:
      | project_title | todo_title    |
      | Project A     | Todo 1        |
      | Project B     | Todo 2        |
      | Project C     | Todo 3        |

  Scenario Outline: Successfully add multiple tasks to a project
    Given a project with title "{project_title}" exists
    When I have todo items with titles "Todo 1" "Todo 2" "Todo 3"
    And I add the todos to the project
    Then the project should contain the todos

    Examples:
      | project_title |
      | Project X     |
      | Project Y     |

  Scenario Outline: Fail to add a non-existing task to a project
    Given a project with title "{project_title}" exists
    When I attempt to add a non-existing todo with id "<todo_id>" to the project
    Then the response should contain an error message indicating the todo does not exist

    Examples:
      | project_title | todo_id |
      | Project Error | 9999    |
      | Project Error | 8888    |
