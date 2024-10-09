from base_test import BaseAPITest, require_service_running


class TestProjectsUndocumented(BaseAPITest):

    @require_service_running
    def test_put_on_projects_endpoint(self):
        """Test PUT /projects is not allowed and returns 405."""
        payload = {"title": "Should not be allowed"}
        response = self.session.put(
            f"{self.BASE_URL}/projects", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_patch_on_projects_endpoint(self):
        """Test PATCH /projects is not allowed and returns 405."""
        payload = {"title": "Should not be allowed"}
        response = self.session.patch(
            f"{self.BASE_URL}/projects", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 405)

    @require_service_running
    def test_invalid_projects_endpoint(self):
        """Test accessing an invalid endpoint under /projects returns 404."""
        response = self.session.get(
            f"{self.BASE_URL}/projects/invalid_endpoint", headers=self.HEADERS_JSON
        )
        self.assertEqual(response.status_code, 404)

    @require_service_running
    def test_post_on_projects_id_endpoint(self):
        """Test POST /projects/:id is allowed for amending (as per documentation)."""
        # Create a project first
        project = self.create_project(title="Amend Test Project")
        project_id = project["id"]

        # Amend the project
        payload = {"title": "Amended Project Title"}
        response = self.session.post(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Amended Project Title")

    @require_service_running
    def test_post_on_projects_id_with_invalid_field(self):
        """Test POST /projects/:id with invalid field returns 400."""
        # Create a project first
        project = self.create_project(title="Invalid Field Test Project")
        project_id = project["id"]

        # Attempt to amend with an invalid field
        payload = {"badfield": "This should not be allowed"}
        response = self.session.post(
            f"{self.BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.HEADERS_JSON,
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errorMessages", data)
        self.assertIn("Could not find field: badfield", data["errorMessages"])
