Feature: Create a new todo item
  As a user, I want to create a new todo item by providing a title so that I can track my tasks.

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Create a new todo item with a valid title
    When I create a new todo with only title "<title>"
    Then the todo item should be created with only title "<title>"

    Examples:
      | title         |
      | Buy groceries |
      | Call Mom      |
      | Finish report |

  Scenario Outline: Create a new todo item with title and description
    When I create a new todo with title "<title>" and description "<description>"
    Then the todo item should be created with title "<title>" and description "<description>"

    Examples:
      | title      | description                            |
      | Read book  | Read 'Clean Code' by Robert C. Martin  |
      | Write blog | Write a post about BDD with Gherkin    |
      | Plan trip  | Plan itinerary for the summer vacation |

  Scenario Outline: Fail to create a new todo item without a title
    When I attempt to create a new todo without a title
    Then the todo item should not be created
    And I should receive an error message "<error_message>" indicating the title field is mandatory

    Examples:
      | error_message              |
      | title : field is mandatory |
