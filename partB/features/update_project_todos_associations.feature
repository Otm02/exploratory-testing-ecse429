Feature: Modify Project-Todo Associations
  As a user, I want to modify existing associations between projects and todos, so that I can update how tasks are organized within projects

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully update a project's todo association
    Given a project with title "<project_title>" exists

    And a todo item with title "<old_todo_title>" exists
    And I add the todo to the project
    And a todo item with title "<new_todo_title>" exists

    When I replace the todo "<old_todo_title>" with "<new_todo_title>" in the project
    Then the project should contain the todo "<new_todo_title>"
    And the project should not contain the todo "<old_todo_title>"

    Examples:
      | project_title | old_todo_title | new_todo_title |
      | Project A     | Todo 1         | Todo A         |
      | Project B     | Todo 2         | Todo B         |
      | Project C     | Todo 3         | Todo C         |

  Scenario Outline: Successfully add multiple new todos to a project while removing old ones
    Given a project with title "<project_title>" exists

    And a todo item with title "<old_todo1>" exists
    And I add the todo to the project
    And a todo item with title "<old_todo2>" exists

    When I add the todo to the project
    And a todo item with title "<new_todo1>" exists
    And a todo item with title "<new_todo2>" exists
    And I update the project's todos to "<new_todo1>" and "<new_todo2>"

    Then the project should contain the todos "<new_todo1>" and "<new_todo2>"
    And the project should not contain the todos "<old_todo1>" and "<old_todo2>"

    Examples:
      | project_title | old_todo1 | old_todo2 | new_todo1 | new_todo2 |
      | Project X     | Old Todo 1 | Old Todo 2 | New Todo 1 | New Todo 2 |
      | Project Y     | Old Todo A | Old Todo B | New Todo A | New Todo B |

  Scenario Outline: Fail to update project with a non-existing todo
    Given a project with title "<project_title>" exists
    And a todo item with title "<existing_todo_title>" exists
    And I add the todo to the project
    
    When I attempt to replace the todo "<existing_todo_title>" with non-existing todo id "<non_existing_todo_id>"
    Then the response should contain an error message indicating the todo does not exist

    Examples:
      | project_title | existing_todo_title | non_existing_todo_id |
      | Project Error | Todo X              | 9999                 |
      | Project Error | Todo Y              | 8888                 |
