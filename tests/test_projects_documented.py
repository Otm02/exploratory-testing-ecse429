from base_test import BaseAPITest, require_service_running


class TestProjectsDocumented(BaseAPITest):

    @require_service_running
    def test_get_all_projects_json(self):
        """Test GET /projects returns all projects in JSON format."""
        response = self.session.get(
            f"{self.BASE_URL}/projects", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("projects", data)
        self.assertIsInstance(data["projects"], list)

    @require_service_running
    def test_get_all_projects_xml(self):
        """Test GET /projects returns all projects in XML format."""
        response = self.session.get(
            f"{self.BASE_URL}/projects", headers=self.HEADERS_XML
        )
        self.assertEqual(response.status_code, 200)
        data = self.parse_xml(response.text)
        self.assertEqual(data.tag, "projects", "Root element is not 'projects'")

    @require_service_running
    def test_create_project_with_fields_json(self):
        """Test POST /projects creates a project with provided fields (JSON)."""
        # Use create_project utility to ensure tracking
        project = self.create_project(
            title="Test Project",
            completed=False,
            active=True,
            description="Project description.",
        )
        # Assertions are already handled in create_project
        self.assertIn("id", project)
        self.assertEqual(project["title"], "Test Project")
        self.assertEqual(project["completed"], "false")
        self.assertEqual(project["active"], "true")
        self.assertEqual(project["description"], "Project description.")

    @require_service_running
    def test_create_project_with_fields_xml(self):
        """Test POST /projects creates a project with provided fields (XML)."""
        xml_payload = """
        <project>
            <title>Test Project XML</title>
            <completed>false</completed>
            <active>true</active>
            <description>Project description XML.</description>
        </project>
        """
        response = self.send_xml_post("/projects", xml_payload)
        self.assertEqual(response.status_code, 201)
        data = self.parse_xml(response.text)
        project_id = data.find("id").text
        # Track the created project
        self.created_projects.append(project_id)
        self.assertIsNotNone(project_id)
        self.assertEqual(data.find("title").text, "Test Project XML")
        self.assertEqual(data.find("completed").text, "false")
        self.assertEqual(data.find("active").text, "true")
        self.assertEqual(data.find("description").text, "Project description XML.")

    @require_service_running
    def test_get_project_by_id_json(self):
        """Test GET /projects/:id returns the correct project (JSON)."""
        # Create a project first
        project = self.create_project(title="Unique Test Project")
        project_id = project["id"]

        # Retrieve the project by ID
        response = self.session.get(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("projects", data)
        self.assertEqual(len(data["projects"]), 1)
        self.assertEqual(data["projects"][0]["id"], project_id)
        self.assertEqual(data["projects"][0]["title"], "Unique Test Project")

    @require_service_running
    def test_get_project_by_id_xml(self):
        """Test GET /projects/:id returns the correct project (XML)."""
        # Create a project first
        project = self.create_project(title="Unique Test Project XML")
        project_id = project["id"]

        # Retrieve the project by ID
        response = self.session.get(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(response.status_code, 200)
        data = self.parse_xml(response.text)
        print(response.text)

        # Access the <project> element
        project_element = data.find("project")
        self.assertIsNotNone(
            project_element, "Project element not found in XML response."
        )

        # Verify the root tag
        self.assertEqual(data.tag, "projects")

        # Verify the <id> element
        id_element = project_element.find("id")
        self.assertIsNotNone(id_element, "ID element not found in project.")
        self.assertEqual(id_element.text, str(project_id), "Project ID does not match.")

        # Verify the <title> element
        title_element = project_element.find("title")
        self.assertIsNotNone(title_element, "Title element not found in project.")
        self.assertEqual(
            title_element.text,
            "Unique Test Project XML",
            "Project title does not match.",
        )

    @require_service_running
    def test_delete_project_json(self):
        """Test DELETE /projects/:id deletes the project (JSON)."""
        # Create a project to delete
        project = self.create_project(title="To be deleted Project JSON")
        project_id = project["id"]

        # Delete the project
        response = self.session.delete(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        # Remove from tracking since it's already deleted
        self.created_projects.remove(project_id)

        # Confirm deletion
        get_response = self.session.get(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(get_response.status_code, 404)
        data = get_response.json()
        self.assertIn("errorMessages", data)

    @require_service_running
    def test_delete_project_xml(self):
        """Test DELETE /projects/:id deletes the project (XML)."""
        # Create a project to delete
        project = self.create_project(title="To be deleted Project XML")
        project_id = project["id"]

        # Delete the project
        response = self.session.delete(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(response.status_code, 200)
        # Remove from tracking since it's already deleted
        self.created_projects.remove(project_id)

        # Confirm deletion
        get_response = self.session.get(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_XML
        )
        self.assertEqual(get_response.status_code, 404)
        self.assertIn("errorMessages", get_response.text)

    @require_service_running
    def test_put_project_update_fields_json(self):
        """Test PUT /projects/:id updates the project fields (JSON)."""
        # Create a project
        project = self.create_project(
            title="Original Title", description="Original Description"
        )
        project_id = project["id"]

        # Update the project
        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True,
            "active": False,
        }
        response = self.session.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["description"], "Updated Description")
        self.assertEqual(data["completed"], "true")
        self.assertEqual(data["active"], "false")

    @require_service_running
    def test_put_project_update_fields_xml(self):
        """Test PUT /projects/:id updates the project fields (XML)."""
        # Create a project
        project = self.create_project(
            title="Original Title XML", description="Original Description XML"
        )
        project_id = project["id"]

        # Update the project
        xml_payload = f"""
        <project>
            <id>{project_id}</id>
            <title>Updated Title XML</title>
            <description>Updated Description XML</description>
            <completed>true</completed>
            <active>false</active>
        </project>
        """
        response = self.send_xml_put(f"/projects/{project_id}", xml_payload)
        self.assertEqual(response.status_code, 200)
        data = self.parse_xml(response.text)
        self.assertEqual(data.find("title").text, "Updated Title XML")
        self.assertEqual(data.find("description").text, "Updated Description XML")
        self.assertEqual(data.find("completed").text, "true")
        self.assertEqual(data.find("active").text, "false")

    @require_service_running
    def test_put_project_change_id_not_allowed_json(self):
        """Test PUT /projects/:id with ID change is not allowed (JSON)."""
        # Create a project
        project = self.create_project(title="ID Change Test Project")
        project_id = project["id"]

        # Attempt to change the ID
        payload = {"id": "9999", "title": "ID Changed Title"}
        response = self.session.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn("Failed Validation: id should be ID", data["errorMessages"])

    @require_service_running
    def test_head_projects(self):
        """Test HEAD /projects returns headers."""
        response = self.session.head(f"{self.BASE_URL}/projects")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Type", response.headers)

    @require_service_running
    def test_head_project_by_id(self):
        """Test HEAD /projects/:id returns headers."""
        # Create a project first
        project = self.create_project(title="HEAD Test Project")
        project_id = project["id"]

        # Retrieve headers
        response = self.session.head(
            f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Type", response.headers)

    @require_service_running
    def test_head_nonexistent_project(self):
        """Test HEAD /projects/:id with invalid ID returns 404."""
        invalid_id = "423q243raz"
        response = self.session.head(
            f"{self.BASE_URL}/projects/{invalid_id}", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 404)
