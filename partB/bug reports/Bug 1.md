# Bug Report 1: Associations Persist After Deletion of Todo Item

**Date:** 11/01/2024 - 11:45 AM  
**Reported by:** Athmane  
**Scenario:** Delete a todo item associated with a project and category  
**Endpoint:** `/todos/{todo_id}/tasksof`, `/todos/{todo_id}/categories`
**Method:** `GET`

## Executive Summary

When a todo item associated with a project and category is deleted, the API should ensure all associations with projects and categories are removed. However, the associations still exist after deletion, violating expected behavior.

## Description

In the scenario where a todo item with associations to a project and a category is deleted, the API continues to return valid responses for these associations. Specifically, a `GET` request to `/todos/{todo_id}/tasksof` and `/todos/{todo_id}/categories` returns data, whereas it should return a `404 Not Found` indicating the todo item and its associations have been fully removed.

## Potential Impact

-   Clients may assume the todo item and its associations still exist after deletion, leading to inconsistent application state.
-   This issue may impact data integrity, as deleted items should not retain associations.

## Steps to Reproduce

1.  **Create a todo item and associate it with a project and category.**
2.  **Delete the todo item.**
3.  **Send a `GET` request to `/todos/{todo_id}/tasksof`:**
    - Expected: `404 Not Found`
    - Actual: Response indicates association still exists.
4.  **Send a `GET` request to `/todos/{todo_id}/categories`:**
    - Expected: `404 Not Found`
    - Actual: Response indicates association still exists.