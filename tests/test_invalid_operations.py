from base_test import BaseAPITest, require_service_running


class TestInvalidOperations(BaseAPITest):

    @require_service_running
    def test_delete_nonexistent_todo(self):
        """Test DELETE /todos/:id on a nonexistent todo returns 404."""
        invalid_id = "999999"
        response = self.session.delete(
            f"{self.BASE_URL}/todos/{invalid_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code, 404, msg=f"Expected 404, got {response.status_code}"
        )

        data = response.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Could not find any instances with todos/{invalid_id}" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_delete_already_deleted_todo(self):
        """Test DELETE /todos/:id on a todo that has already been deleted returns 404."""
        # Create a todo
        todo = self.create_todo(title="Delete Twice Test TODO")
        todo_id = todo["id"]

        # Delete the todo
        delete_response = self.session.delete(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            delete_response.status_code,
            200,
            msg=f"Expected 200, got {delete_response.status_code}",
        )

        # Attempt to delete again
        delete_response_again = self.session.delete(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            delete_response_again.status_code,
            404,
            msg=f"Expected 404, got {delete_response_again.status_code}",
        )

        data = delete_response_again.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Could not find any instances with todos/{todo_id}" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_delete_nonexistent_project(self):
        """Test DELETE /projects/:id on a nonexistent project returns 404."""
        invalid_id = "999999"
        response = self.session.delete(
            f"{self.BASE_URL}/projects/{invalid_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code, 404, msg=f"Expected 404, got {response.status_code}"
        )

        data = response.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Could not find any instances with projects/{invalid_id}" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_delete_already_deleted_project(self):
        """Test DELETE /projects/:id on a project that has already been deleted returns 404."""
        # Create a project
        project = self.create_project(title="Delete Twice Test Project")
        project_id = project["id"]

        # Delete the project
        delete_response = self.session.delete(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            delete_response.status_code,
            200,
            msg=f"Expected 200, got {delete_response.status_code}",
        )

        # Attempt to delete again
        delete_response_again = self.session.delete(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(
            delete_response_again.status_code,
            404,
            msg=f"Expected 404, got {delete_response_again.status_code}",
        )

        data = delete_response_again.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Could not find any instances with projects/{project_id}" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_update_nonexistent_todo(self):
        """Test PUT /todos/:id on a nonexistent todo returns 404."""
        invalid_id = "999999"
        payload = {"title": "Attempt to Update Nonexistent TODO"}
        response = self.session.put(
            f"{self.BASE_URL}/todos/{invalid_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(
            response.status_code, 404, msg=f"Expected 404, got {response.status_code}"
        )

        data = response.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Invalid GUID for {invalid_id} entity todo" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_update_nonexistent_project(self):
        """Test PUT /projects/:id on a nonexistent project returns 404."""
        invalid_id = "999999"
        payload = {"title": "Attempt to Update Nonexistent Project"}
        response = self.session.put(
            f"{self.BASE_URL}/projects/{invalid_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(
            response.status_code, 404, msg=f"Expected 404, got {response.status_code}"
        )

        data = response.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertTrue(
            any(
                f"Invalid GUID for {invalid_id} entity project" in msg
                for msg in error_messages
            ),
            f"Expected error message not found. Received: {error_messages}",
        )
