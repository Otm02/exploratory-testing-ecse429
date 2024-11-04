Feature: Associate Project With Tasks
  As a user, I want to manage tasks within a project, so that I can organize tasks under specific projects

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully add a task to a project
    Given a project with title "<project_title>" exists
    And a todo item with title "<todo_title>" exists
    When I add the todo to the project
    Then the project should contain the todo

    Examples:
      | project_title | todo_title    |
      | Project A     | Todo 1        |
      | Project B     | Todo 2        |
      | Project C     | Todo 3        |

  Scenario Outline: Successfully add multiple tasks to a project
    Given a project with title "<project_title>" exists
    When todo items with titles "<todo_1>" "<todo_2>" "<todo_3>" exist and are associated to project
    Then the project should contain the todos

    Examples:
      | project_title | todo_1 | todo_2 | todo_3 |
      | Project X     | x1     | x2     | x3     |
      | Project Y     | y1     | y2     | y3     |

  Scenario Outline: Fail to add a non-existing task to a project
    Given a project with title "<project_title>" exists
    When I attempt to add a non-existing todo with id "<todo_id>" to the project
    Then the response should contain an error message indicating the todo does not exist

    Examples:
      | project_title | todo_id |
      | Project Error | 9999    |
      | Project Error | -1      |
