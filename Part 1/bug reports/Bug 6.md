
# Bug Report 6: GET `/projects/{invalidID}/tasks` Returns Empty List Instead of Error

**Date:** 06/10/2024 - 3:50 PM  
**Reported by:** Alec  
**Endpoint:** `/projects/invalidID/tasks`  
**Method:** `GET`

## Executive Summary

When requesting tasks for a non-existent project ID, the API returns a `200 OK` status with an empty list instead of a `404 Not Found` error.

## Description

A `GET` request to `/projects/{invalidID}/tasks` should return an error if the project ID does not exist. Instead, the API responds with an empty `tasks` list.

## Potential Impact

-   Clients may incorrectly assume the project exists without tasks.

## Steps to Reproduce

1.  **Send a `GET` request to `/projects/invalidID/tasks`:**
    
2.  **Observe the response:**
    
    `{
      "tasks": []
    }` 
    
3.  **Note the status code `200 OK` and lack of an error message.**