from base_test import BaseAPITest, require_service_running


class TestTodosUndocumented(BaseAPITest):

    @require_service_running
    def test_put_on_todos_endpoint(self):
        """Test PUT /todos is not allowed and returns 405."""
        payload = {"title": "Should not be allowed"}
        response = self.session.put(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_patch_on_todos_endpoint(self):
        """Test PATCH /todos is not allowed and returns 405."""
        payload = {"title": "Should not be allowed"}
        response = self.session.patch(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_invalid_endpoint(self):
        """Test accessing an invalid endpoint under /todos returns 404."""
        response = self.session.get(
            f"{self.BASE_URL}/todos/invalid_endpoint", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 404)

    @require_service_running
    def test_post_on_todos_id_endpoint(self):
        """Test POST /todos/:id is allowed for amending (as per documentation)."""
        # Create a todo first
        todo = self.create_todo(title="Amend Test TODO")
        todo_id = todo["id"]

        # Amend the todo
        payload = {"title": "Amended Title"}
        response = self.session.post(
            f"{self.BASE_URL}/todos/{todo_id}", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Amended Title")

    @require_service_running
    def test_post_on_todos_id_with_invalid_field(self):
        """Test POST /todos/:id with invalid field returns 400."""
        # Create a todo first
        todo = self.create_todo(title="Invalid Field Test TODO")
        todo_id = todo["id"]

        # Attempt to amend with an invalid field
        payload = {"badfield": "This should not be allowed"}
        response = self.session.post(
            f"{self.BASE_URL}/todos/{todo_id}", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn("Could not find field: badfield", data["errorMessages"])
