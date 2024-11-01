from base_test import BaseAPITest, require_service_running


class TestBugs(BaseAPITest):
    @require_service_running
    def test_bug_get_todos_with_invalid_id_categories_returns_empty_json(self):
        """
        Bug: GET /todos/:id/categories with invalid ID returns empty list instead of error message.
        Expected: 404 Not Found with error message.
        Actual: 200 OK with empty list.
        """
        invalid_id = "423q243raz"
        response = self.session.get(
            f"{self.BASE_URL}/todos/{invalid_id}/categories", headers=self.HEADERS_JSON
        )

        # Expected Behavior
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn(
            f"Could not find an instance with todos/{invalid_id}",
            data["errorMessages"],
        )

    @require_service_running
    def test_bug_get_todos_with_invalid_id_tasksof_returns_empty_json(self):
        """
        Bug: GET /todos/:id/tasksof with invalid ID returns empty list instead of error message.
        Expected: 404 Not Found with error message.
        Actual: 200 OK with empty list.
        """
        invalid_id = "423q243raz"
        response = self.session.get(
            f"{self.BASE_URL}/todos/{invalid_id}/tasksof", headers=self.HEADERS_JSON
        )

        # Expected Behavior
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn(
            f"Could not find an instance with todos/{invalid_id}",
            data["errorMessages"],
        )

    @require_service_running
    def test_bug_get_projects_with_invalid_id_categories_returns_empty_json(self):
        """
        Bug: GET /projects/:id/categories with invalid ID returns empty list instead of error message.
        Expected: 404 Not Found with error message.
        Actual: 200 OK with empty list.
        """
        invalid_id = "423q243raz"
        response = self.session.get(
            f"{self.BASE_URL}/projects/{invalid_id}/categories",
            headers=self.HEADERS_JSON,
        )

        # Expected Behavior
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn(
            f"Could not find an instance with projects/{invalid_id}",
            data["errorMessages"],
        )

    @require_service_running
    def test_bug_get_projects_with_invalid_id_tasks_returns_empty_json(self):
        """
        Bug: GET /projects/:id/tasks with invalid ID returns empty list instead of error message.
        Expected: 404 Not Found with error message.
        Actual: 200 OK with empty list.
        """
        invalid_id = "423q243raz"
        response = self.session.get(
            f"{self.BASE_URL}/projects/{invalid_id}/tasks", headers=self.HEADERS_JSON
        )

        # Expected Behavior
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn(
            f"Could not find an instance with projects/{invalid_id}",
            data["errorMessages"],
        )

    @require_service_running
    def test_bug_put_project_with_unspecified_fields_replaced(self):
        """
        Bug: PUT /projects/:id with unspecified fields are replaced with default values instead of remaining unchanged.
        Expected: Unspecified fields remain unchanged.
        Actual: Unspecified fields are replaced with default values.
        """
        # Create a project
        project = self.create_project(
            title="Original Project",
            completed=True,
            active=True,
            description="Original Description",
        )
        project_id = project["id"]

        # Perform PUT with only 'title' field
        payload = {"title": "Updated Project Title"}
        response = self.session.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Expected Behavior
        self.assertEqual(data["title"], "Updated Project Title")
        self.assertEqual(data["completed"], "true")
        self.assertEqual(data["active"], "true")
        self.assertEqual(data["description"], "Original Description")

    @require_service_running
    def test_bug_put_project_data_type_inconsistency(self):
        """
        Bug: PUT /projects/:id has data type inconsistency for 'completed' and 'active' fields.
        Expected: Data types should be consistent (BOOLEAN).
        Actual: Data types differ (strings instead of booleans).
        """
        # Create a project
        project = self.create_project(
            title="Data Type Test Project", completed=False, active=True
        )
        project_id = project["id"]

        # Perform PUT to update 'completed' and 'active'
        payload = {"completed": "true", "active": "false"}
        response = self.session.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Expected Behavior
        self.assertIsInstance(data["completed"], bool)
        self.assertIsInstance(data["active"], bool)
