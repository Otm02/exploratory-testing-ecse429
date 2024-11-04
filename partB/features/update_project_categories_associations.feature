Feature: Modify Project-Category Associations
  As a user, I want to modify existing associations between projects and categories, so that I can update how categories are organized within projects

  Background:
    Given the todo list application is running
    And the database contains the default todo objects

  Scenario Outline: Successfully update a project's category association
    Given a project with title "<project_title>" exists
    And a category with title "<old_category_title>" exists

    When I add the category to the project
    And a category with title "<new_category_title>" exists
    And I replace the category "<old_category_title>" with "<new_category_title>" in the project

    Then the project should contain the category "<new_category_title>"
    And the project should not contain the category "<old_category_title>"

    Examples:
      | project_title | old_category_title | new_category_title |
      | Project A     | Category 1         | Category A         |
      | Project B     | Category 2         | Category B         |
      | Project C     | Category 3         | Category C         |

  Scenario Outline: Successfully add multiple new categories to a project while removing old ones
    Given a project with title "<project_title>" exists
    And a category with title "<old_category1>" exists
    And I add the category to the project
    And a category with title "<old_category2>" exists
    And I add the category to the project
    And a category with title "<new_category1>" exists
    And a category with title "<new_category2>" exists

    When I update the project's categories to "<new_category1>" and "<new_category2>"
    Then the project should contain the categories "<new_category1>" and "<new_category2>"
    And the project should not contain the categories "<old_category1>" and "<old_category2>"

    Examples:
      | project_title | old_category1 | old_category2 | new_category1 | new_category2 |
      | Project X     | Old Cat 1     | Old Cat 2     | New Cat 1     | New Cat 2     |
      | Project Y     | Old Cat A     | Old Cat B     | New Cat A     | New Cat B     |

  Scenario Outline: Fail to update project with a non-existing category
    Given a project with title "<project_title>" exists
    And a category with title "<existing_category_title>" exists
    And I add the category to the project

    When I attempt to replace the category "<existing_category_title>" with non-existing category id "<non_existing_category_id>"
    Then the response should contain an error message indicating the category does not exist

    Examples:
      | project_title | existing_category_title | non_existing_category_id |
      | Project Error | Category X              | 9999                     |
      | Project Error | Category Y              | 8888                     |
