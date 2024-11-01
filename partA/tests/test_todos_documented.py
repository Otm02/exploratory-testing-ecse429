from base_test import BaseAPITest, require_service_running


class TestTodosDocumented(BaseAPITest):

    @require_service_running
    def test_get_all_todos_json(self):
        """Test GET /todos returns all todos in JSON format."""
        response = self.session.get(f"{self.BASE_URL}/todos", headers=self.HEADERS_JSON)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("todos", data)
        self.assertIsInstance(data["todos"], list)

    @require_service_running
    def test_get_all_todos_xml(self):
        """Test GET /todos returns all todos in XML format."""
        response = self.session.get(f"{self.BASE_URL}/todos", headers=self.HEADERS_XML)
        self.assertEqual(response.status_code, 200)
        data = self.parse_xml(response.text)
        # Check if 'todos' key exists or if 'todo' is a list or None
        if data.tag == "todos":
            # Assuming 'todos' contains multiple 'todo' elements
            todos = data.findall("todo")
            self.assertIsInstance(todos, list)
        elif data.tag == "todo":
            # Single 'todo' element
            self.assertIsNotNone(data, "No 'todo' element found in the response.")
        else:
            self.fail("Response XML does not contain 'todos' or 'todo' elements.")

    @require_service_running
    def test_create_todo_with_title_json(self):
        """Test POST /todos creates a todo when title is provided (JSON)."""
        # Use create_todo utility to ensure tracking
        todo = self.create_todo(title="Test TODO")
        self.assertIn("id", todo)
        self.assertEqual(todo["title"], "Test TODO")
        self.assertEqual(
            todo["doneStatus"], "false"
        )  # Expecting string as per API response
        self.assertEqual(todo["description"], "")  # Handle empty string or None

    @require_service_running
    def test_create_todo_with_title_xml(self):
        """Test POST /todos creates a todo when title is provided (XML)."""
        xml_payload = """
        <todo>
            <title>Test TODO</title>
            <doneStatus>false</doneStatus>
            <description></description>
        </todo>
        """
        response = self.send_xml_post("/todos", xml_payload)
        self.assertEqual(response.status_code, 201)
        data = self.parse_xml(response.text)
        todo_id = data.find("id").text
        # Track the created todo
        self.created_todos.append(todo_id)
        self.assertIsNotNone(todo_id, "No 'id' element found in the response.")
        self.assertEqual(data.find("title").text, "Test TODO")
        self.assertEqual(data.find("doneStatus").text, "false")
        description = data.find("description").text
        self.assertTrue(
            description == "" or description is None,
            "Description should be empty or None.",
        )

    @require_service_running
    def test_create_todo_without_title_json(self):
        """Test POST /todos without title returns an error (JSON)."""
        payload = {
            "doneStatus": False,  # Send as boolean
            "description": "No title provided.",
        }
        response = self.session.post(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.get("errorMessages") or [data.get("errorMessage")]
        self.assertIsNotNone(error_messages, "No error messages found in the response.")
        self.assertIn("title : field is mandatory", error_messages)

    @require_service_running
    def test_create_todo_without_title_xml(self):
        """Test POST /todos without title returns an error (XML)."""
        xml_payload = """
        <todo>
            <doneStatus>false</doneStatus>
            <description>No title provided.</description>
        </todo>
        """
        response = self.send_xml_post("/todos", xml_payload)
        self.assertEqual(response.status_code, 400)
        data = self.parse_xml(response.text)
        # Handle both 'errorMessages' and 'errorMessage'
        error_messages = data.find("errorMessages")
        if error_messages is None:
            error_message = data.find("errorMessage")
            error_messages = [error_message.text] if error_message is not None else []
        else:
            error_messages = [em.text for em in error_messages.findall("errorMessage")]
        self.assertTrue(
            len(error_messages) > 0, "No error messages found in the response."
        )
        self.assertIn("title : field is mandatory", error_messages)

    @require_service_running
    def test_get_todo_by_id_json(self):
        """Test GET /todos/:id returns the correct todo (JSON)."""
        # Create a todo first
        todo = self.create_todo(title="Unique Test TODO")
        todo_id = todo["id"]

        # Retrieve the todo by ID
        response = self.session.get(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("todos", data)
        self.assertEqual(len(data["todos"]), 1)
        self.assertEqual(data["todos"][0]["id"], todo_id)
        self.assertEqual(data["todos"][0]["title"], "Unique Test TODO")

    @require_service_running
    def test_get_todo_by_id_xml(self):
        """Test GET /todos/:id returns the correct todo (XML)."""
        # Create a todo first
        todo = self.create_todo(title="Unique Test TODO XML")
        todo_id = todo["id"]

        # Retrieve the todo by ID
        response = self.session.get(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(response.status_code, 200)
        data = self.parse_xml(response.text)
        todo_element = data.find("todo")
        self.assertIsNotNone(todo_element, "No 'todo' element found in the response.")
        id_element = todo_element.find("id")
        self.assertIsNotNone(id_element, "No 'id' element found within 'todo'.")
        self.assertEqual(id_element.text, todo_id)
        title_element = todo_element.find("title")
        self.assertIsNotNone(title_element, "No 'title' element found within 'todo'.")
        self.assertEqual(title_element.text, "Unique Test TODO XML")

    @require_service_running
    def test_delete_todo_json(self):
        """Test DELETE /todos/:id deletes the todo (JSON)."""
        # Create a todo to delete
        todo = self.create_todo(title="To be deleted JSON")
        todo_id = todo["id"]

        # Delete the todo
        response = self.session.delete(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        # Remove from tracking since it's already deleted
        self.created_todos.remove(todo_id)

        # Confirm deletion
        get_response = self.session.get(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(get_response.status_code, 404)
        data = get_response.json()
        self.assertIn("errorMessages", data)

    @require_service_running
    def test_delete_todo_xml(self):
        """Test DELETE /todos/:id deletes the todo (XML)."""
        # Create a todo to delete
        todo = self.create_todo(title="To be deleted XML")
        todo_id = todo["id"]

        # Delete the todo
        response = self.session.delete(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(response.status_code, 200)
        # Remove from tracking since it's already deleted
        self.created_todos.remove(todo_id)

        # Confirm deletion
        get_response = self.session.get(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(get_response.status_code, 404)
        data = self.parse_xml(get_response.text)
        error_element = data.find("errorMessages")
        if error_element is None:
            error_message = data.find("errorMessage")
            error_messages = [error_message.text] if error_message is not None else []
        else:
            error_messages = [em.text for em in error_element.findall("errorMessage")]
        self.assertTrue(
            len(error_messages) > 0, "No error messages found in the response."
        )
        self.assertIn(
            f"Could not find an instance with todos/{todo_id}", error_messages
        )

    @require_service_running
    def test_put_todo_not_allowed(self):
        """Test PUT /todos is not allowed as per documentation."""
        payload = {"title": "Should not be allowed"}
        response = self.session.put(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_patch_todo_not_allowed(self):
        """Test PATCH /todos is not allowed as per documentation."""
        payload = {"title": "Should not be allowed"}
        response = self.session.patch(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_head_todos(self):
        """Test HEAD /todos returns headers."""
        response = self.session.head(f"{self.BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Type", response.headers)

    @require_service_running
    def test_head_todo_by_id(self):
        """Test HEAD /todos/:id returns headers."""
        # Create a todo first
        todo = self.create_todo(title="HEAD Test TODO")
        todo_id = todo["id"]

        # Retrieve headers
        response = self.session.head(
            f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Type", response.headers)

    @require_service_running
    def test_head_nonexistent_todo(self):
        """Test HEAD /todos/:id with invalid ID returns 404."""
        invalid_id = "423q243raz"
        response = self.session.head(
            f"{self.BASE_URL}/todos/{invalid_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 404)
