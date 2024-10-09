# Bug Report 2: GET `/todos/{invalidID}/tasksof` Returns All Projects

**Date:** 06/10/2024 - 12:32 PM  
**Reported by:** Athmane  
**Endpoint:** `/todos/invalidID/tasksof`  
**Method:** `GET`

## Executive Summary

Requesting projects for an invalid todo ID returns all projects instead of an error.

## Description

A `GET` request to `/todos/invalidID/tasksof` with an invalid todo ID should return a `404 Not Found` error. However, the API responds with a `200 OK` status and returns a list of all projects in the system.

## Potential Impact

-   Unintended exposure of all projects.
-   Clients may misinterpret the data.

## Steps to Reproduce

1.  **Send a `GET` request to `/todos/invalidID/tasksof`:**
    
2.  **Observe the response containing all projects:**

    `{
      "projects": [
        {
          "id": "16",
          "title": "title 222ee",
          "completed": "false",
          "active": "false",
          "description": "desc 2",
          "tasks": [{"id": "2"}]
        },
        // ... other projects
      ]
    }` 
    
3.  **Note that the status code is `200 OK` instead of a `404 Not Found`.**