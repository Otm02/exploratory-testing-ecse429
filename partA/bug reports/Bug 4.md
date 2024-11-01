
# Bug Report 4: `POST` to `/projects/{id}/tasks` Does Not Return the Created Relationship

**Date:** 06/10/2024 - 3:07 PM  
**Reported by:** Athmane  
**Endpoint:** `/projects/1/tasks`  
**Method:** `POST`

## Executive Summary

Adding a task relationship to a project does not return the new relationship in the response body.

## Description

After successfully adding a task to a project using `POST`, the API responds with a `201 Created` status but does not include the details of the created relationship.

## Potential Impact

-   **Uncertainty:** Clients cannot confirm the addition of the relationship.

## Steps to Reproduce

1.  **Send a `POST` request to `/projects/1/tasks` with the following JSON payload:**
    
    `{
      "id": "1"
    }` 
    
2.  **Observe the response:**
    
    -   **Status Code:** `201 Created`
    -   **Response Body:** Empty
3.  **Note the absence of the new relationship details in the response.**