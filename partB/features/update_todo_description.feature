Feature: Update the description of an existing todo item
  As a user, I want to update the description of an existing todo item so that I can provide more details about the task.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully update the description of an existing todo item
    Given a todo item with title "<todo_title>" exists
    When I update the description of the todo item with title "<todo_title>" to "<new_description>"
    Then the todo item should have description "<new_description>"

    Examples:
      | todo_title    | new_description          |
      | Buy groceries | Milk, Eggs, Bread        |
      | Clean house   | Vacuum and dusting       |
      | Finish report | Complete the final draft |

  Scenario Outline: Update the description and title of an existing todo item
    Given a todo item with title "<current_title>" exists
    When I update the title of the todo item with title "<current_title>" to "<new_title>" and description to "<new_description>"
    Then the todo item should have title "<new_title>" and description "<new_description>"

    Examples:
      | current_title | new_title     | new_description    |
      | Buy groceries | Go shopping   | At the supermarket |
      | Clean house   | Tidy home     | Organize all rooms |
      | Finish report | Submit report | Send to manager    |

  Scenario Outline: Fail to update the description of a non-existent todo item
    When I attempt to update the description of a todo item with id "<invalid_todo_id>" to "<new_description>"
    Then I should receive an error message indicating the todo item does not exist

    Examples:
      | invalid_todo_id | new_description  |
      |            9999 | This should fail |
      |            8888 | Another failure  |
      |            7777 | Yet another fail |
