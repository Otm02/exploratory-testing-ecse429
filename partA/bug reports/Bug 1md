# Bug Report 1: GET `/todos/{invalidID}/categories` Returns 200 OK with Empty List

**Date:** 06/10/2024 - 12:09 PM  
**Reported by:** Athmane  
**Endpoint:** `/todos/1wd/categories`  
**Method:** `GET`

## Executive Summary

The API returns a `200 OK` status with an empty list when requesting categories for a non-existent todo ID.

## Description

When a `GET` request is made to `/todos/1wd/categories` using an invalid todo ID, the API should return a `404 Not Found` error. Instead, it returns a `200 OK` status with an empty `categories` list.

## Potential Impact

-   Clients may incorrectly assume the todo exists without categories.

## Steps to Reproduce

1.  **Send a `GET` request to `/todos/1wd/categories`:**
    
2.  **Observe the response:**

    `{
      "categories": []
    }` 
    
3.  **Note the status code `200 OK` and absence of an error message.**
    