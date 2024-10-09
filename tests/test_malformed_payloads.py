from base_test import BaseAPITest, require_service_running


class TestMalformedPayloads(BaseAPITest):

    @require_service_running
    def test_malformed_json_payload_create_todo(self):
        """Test POST /todos with malformed JSON payload returns 400."""
        malformed_payload = (
            '{"title": "Test TODO", "doneStatus": "false"'  # Missing closing brace
        )
        response = self.session.post(
            f"{self.BASE_URL}/todos", data=malformed_payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )
        try:
            data = response.json()
        except ValueError:
            self.fail("Response is not valid JSON.")

        self.assertIn(
            "errorMessages", data, msg="Response JSON does not contain 'errorMessages'."
        )
        self.assertTrue(
            any(
                "EOFException" in msg or "End of input" in msg
                for msg in data["errorMessages"]
            ),
            f"Expected 'EOFException' or 'End of input' in error messages not found. Received: {data['errorMessages']}",
        )

    @require_service_running
    def test_malformed_json_payload_create_project(self):
        """Test POST /projects with malformed JSON payload returns 400."""
        malformed_payload = (
            '{"title": "Test Project", "completed": "false"'  # Missing closing brace
        )
        response = self.session.post(
            f"{self.BASE_URL}/projects",
            data=malformed_payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )
        try:
            data = response.json()
        except ValueError:
            self.fail("Response is not valid JSON.")

        self.assertIn(
            "errorMessages", data, msg="Response JSON does not contain 'errorMessages'."
        )
        self.assertTrue(
            any(
                "EOFException" in msg or "End of input" in msg
                for msg in data["errorMessages"]
            ),
            f"Expected 'EOFException' or 'End of input' in error messages not found. Received: {data['errorMessages']}",
        )

    @require_service_running
    def test_malformed_xml_payload_create_todo(self):
        """Test POST /todos with malformed XML payload returns 400."""
        malformed_xml = """
        <todo>
            <title>Test TODO</title>
            <doneStatus>false</doneStatus>
            <!-- Missing closing tag for todo -->
        """
        headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
        response = self.session.post(
            f"{self.BASE_URL}/todos", data=malformed_xml, headers=headers
        )
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )

        try:
            data = self.parse_xml(response.text)
        except Exception:
            self.fail("Failed to parse XML response.")

        self.assertEqual(
            data.tag,
            "errorMessages",
            msg=f"Expected root tag 'errorMessages', got '{data.tag}'. Response: {response.text}",
        )

        error_messages = [elem.text for elem in data.findall("errorMessage")]
        self.assertTrue(
            len(error_messages) > 0, "No error messages found in the response."
        )
        self.assertTrue(
            any(
                "Unclosed tag" in msg or "Malformed XML" in msg
                for msg in error_messages
            ),
            f"Expected 'Unclosed tag' or 'Malformed XML' error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_malformed_xml_payload_create_project(self):
        """Test POST /projects with malformed XML payload returns 400."""
        malformed_xml = """
        <project>
            <title>Test Project</title>
            <completed>false</completed>
            <!-- Missing closing tag for project -->
        """
        headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
        response = self.session.post(
            f"{self.BASE_URL}/projects", data=malformed_xml, headers=headers
        )
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )

        try:
            data = self.parse_xml(response.text)
        except Exception:
            self.fail("Failed to parse XML response.")

        self.assertEqual(
            data.tag,
            "errorMessages",
            msg=f"Expected root tag 'errorMessages', got '{data.tag}'. Response: {response.text}",
        )

        error_messages = [elem.text for elem in data.findall("errorMessage")]
        self.assertTrue(
            len(error_messages) > 0, "No error messages found in the response."
        )
        self.assertTrue(
            any(
                "Unclosed tag" in msg or "Malformed XML" in msg
                for msg in error_messages
            ),
            f"Expected 'Unclosed tag' or 'Malformed XML' error message not found. Received: {error_messages}",
        )

    @require_service_running
    def test_malformed_json_payload_update_todo(self):
        """Test PUT /todos/:id with malformed JSON payload returns 400."""
        # Create a todo first
        todo = self.create_todo(title="Malformed JSON Update Test")
        todo_id = todo["id"]

        malformed_payload = (
            '{"title": "Updated TODO", "doneStatus": "true"'  # Missing closing brace
        )
        response = self.session.put(
            f"{self.BASE_URL}/todos/{todo_id}",
            data=malformed_payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )
        try:
            data = response.json()
        except ValueError:
            self.fail("Response is not valid JSON.")

        self.assertIn(
            "errorMessages", data, msg="Response JSON does not contain 'errorMessages'."
        )
        self.assertTrue(
            any(
                "EOFException" in msg or "End of input" in msg
                for msg in data["errorMessages"]
            ),
            f"Expected 'EOFException' or 'End of input' in error messages not found. Received: {data['errorMessages']}",
        )

    @require_service_running
    def test_malformed_xml_payload_update_project(self):
        """Test PUT /projects/:id with malformed XML payload returns 400."""
        # Create a project first
        project = self.create_project(title="Malformed XML Update Test")
        project_id = project["id"]

        malformed_xml = """
        <project>
            <title>Updated Project</title>
            <completed>true</completed>
            <!-- Missing closing tag for project -->
        """
        headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
        response = self.send_xml_put(f"/projects/{project_id}", malformed_xml)
        self.assertEqual(
            response.status_code, 400, msg=f"Expected 400, got {response.status_code}"
        )

        try:
            data = self.parse_xml(response.text)
        except Exception:
            self.fail("Failed to parse XML response.")

        self.assertEqual(
            data.tag,
            "errorMessages",
            msg=f"Expected root tag 'errorMessages', got '{data.tag}'. Response: {response.text}",
        )

        error_messages = [elem.text for elem in data.findall("errorMessage")]
        self.assertTrue(
            len(error_messages) > 0, "No error messages found in the response."
        )
        self.assertTrue(
            any(
                "Unclosed tag" in msg or "Malformed XML" in msg
                for msg in error_messages
            ),
            f"Expected 'Unclosed tag' or 'Malformed XML' error message not found. Received: {error_messages}",
        )
