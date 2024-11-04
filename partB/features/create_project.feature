Feature: Create a New Project
  As a user, I want to create a new project, so that I can organize my tasks under this project

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully create a new project with valid data
    When I create a new project with all fields "<title>" "<completed>" "<active>" "<description>"
    Then the project should be created with all fields "<title>" "<completed>" "<active>" "<description>"

    Examples:
      | title       | completed | active | description    |
      | Title 1     | true      | true   | Description 1  |
      | Title 2     | false     | false  | Description 2  |
      | Title 3     | true      | false  | Description 3  |
      | Title 4     | false     | true   | Description 4  |

  Scenario Outline: Create a project without optional fields
    Given a project with title "<title>" exists
    Then the project should be created with "<title>"
    
    Examples:
      | title       |
      | Title 1     |
      | Title 2     |

  Scenario Outline: Fail to create a project whith fake field
    When I attempt to create a new project with fake field "<fake>"
    Then the response should contain an error message indicating fake field

    Examples:
      | fake |
      | true |
      | false|
      | 123  |

