
# Bug Report 3: GET `/projects/{invalidID}/tasks` Returns All Todos with Duplicates

**Date:** 06/10/2024 - 2:58 PM  
**Reported by:** Athmane  
**Endpoint:** `/projects/1/tasks`  
**Method:** `GET`

## Executive Summary

Requesting tasks for an invalid project ID returns all todo items with duplicates instead of an error.

## Description

A `GET` request to `/projects/{invalidID}/tasks` should return a `404 Not Found` error when the project ID doesn't exist. Instead, the API returns all todo items, some of which are duplicated.

## Potential Impact

-   **Data Leakage:** Unintended exposure of all todo items.

## Steps to Reproduce

1.  **Send a `GET` request to `/projects/1/tasks` with an invalid project ID (assuming '1' is invalid in this context).**
    
2.  **Observe the response containing all todos with duplicates:**
    
    `{
      "todos": [
        { "id": "1", "title": "scan paperwork", /* ... */ },
        { "id": "2", "title": "file paperwork", /* ... */ },
        // Duplicate entries
        { "id": "1", "title": "scan paperwork", /* ... */ }
      ]
    }` 
    
3.  **Note the status code `200 OK` instead of `404 Not Found`.**