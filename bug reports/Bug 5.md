
# Bug Report 5: GET `/projects/{invalidID}/categories` Returns Categories Instead of Error

**Date:** 06/10/2024 - 3:27 PM  
**Reported by:** Alec  
**Endpoint:** `/projects/1/categories`  
**Method:** `GET`

## Executive Summary

Requesting categories for an invalid project ID returns categories instead of a `404 Not Found` error.

## Description

A `GET` request to `/projects/{invalidID}/categories` should return an error if the project ID does not exist. However, the API returns categories as if the project ID were valid.

## Potential Impact

-   **Security Concerns:** Potential exposure of unrelated data.

## Steps to Reproduce

1.  **Send a `GET` request to `/projects/1/categories` with an invalid project ID (assuming '1' is invalid in this context).**
    
2.  **Observe the response:**
    
    `{
      "categories": [
        { "id": "1", "title": "Office", "description": "" }
      ]
    }` 
    
3.  **Note that categories are returned despite the invalid project ID.**