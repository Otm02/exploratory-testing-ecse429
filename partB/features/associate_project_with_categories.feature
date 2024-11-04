Feature: Manage Project Categories
  As a user
  I want to manage categories within a project
  So that I can organize categories under specific projects

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully add a category to a project
    Given a project with title "<project_title>" exists
    And a category with title "<category_title>" exists
    When I add the category to the project
    Then the project should contain the category

    Examples:
      | project_title | category_title |
      | Project A     | Category 1     |
      | Project B     | Category 2     |
      | Project C     | Category 3     |

  Scenario Outline: Successfully add multiple categories to a project
    Given a project with title "<project_title>" exists
    When I have categories with titles "<category1>" "<category2>" "<category3>"
    And I add the categories to the project
    Then the project should contain the categories

    Examples:
      | project_title |
      | Project X     |
      | Project Y     |

  Scenario Outline: Fail to add a non-existing category to a project
    Given a project with title "<project_title>" exists
    When I attempt to add a non-existing category with id "<category_id>" to the project
    Then the response should contain an error message indicating the category does not exist

    Examples:
      | project_title | category_id |
      | Project Error | 9999        |
      | Project Error | 8888        |
