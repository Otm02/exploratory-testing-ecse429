import unittest
import requests
import xml.etree.ElementTree as ET
from functools import wraps


def require_service_running(func):
    """Decorator to skip tests if the API service is not running."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = BaseAPITest.session.get(BaseAPITest.BASE_URL)
            if response.status_code != 200:
                raise Exception("API service is not running.")
        except requests.exceptions.ConnectionError:
            raise unittest.SkipTest("API service is not running.")
        return func(*args, **kwargs)

    return wrapper


class BaseAPITest(unittest.TestCase):
    BASE_URL = "http://localhost:4567"
    HEADERS_JSON = {"Content-Type": "application/json", "Accept": "application/json"}
    HEADERS_XML = {"Content-Type": "application/xml", "Accept": "application/xml"}
    session = requests.Session()

    @classmethod
    def setUpClass(cls):
        """Ensure the API service is running before any tests are executed."""
        try:
            response = cls.session.get(cls.BASE_URL)
            if response.status_code != 200:
                raise Exception("API service is not running.")
        except requests.exceptions.ConnectionError:
            raise Exception("API service is not running.")

    def setUp(self):
        """Set up before each test method."""
        # Initialize lists to keep track of created resources
        self.created_todos = []
        self.created_projects = []
        self.created_categories = []

    def tearDown(self):
        """Clean up after each test method."""
        # Delete any created todos
        for todo_id in self.created_todos:
            self.session.delete(
                f"{self.BASE_URL}/todos/{todo_id}", headers=self.HEADERS_JSON
            )

        # Delete any created projects
        for project_id in self.created_projects:
            self.session.delete(
                f"{self.BASE_URL}/projects/{project_id}", headers=self.HEADERS_JSON
            )

        # Delete any created categories
        for category_id in self.created_categories:
            self.session.delete(
                f"{self.BASE_URL}/categories/{category_id}", headers=self.HEADERS_JSON
            )

    def create_todo(self, title="Test TODO", doneStatus=False, description=""):
        """Utility method to create a TODO."""
        payload = {
            "title": title,
            "doneStatus": doneStatus,
            "description": description,
        }
        response = self.session.post(
            f"{self.BASE_URL}/todos", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code,
            201,
            msg=f"Failed to create TODO: {response.status_code} {response.text}",
        )
        todo = response.json()
        self.created_todos.append(todo["id"])
        return todo

    def create_project(
        self, title="Test Project", completed=False, active=True, description=""
    ):
        """Utility method to create a Project."""
        payload = {
            "title": title,
            "completed": completed,
            "active": active,
            "description": description,
        }
        response = self.session.post(
            f"{self.BASE_URL}/projects", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code,
            201,
            msg=f"Failed to create Project: {response.status_code} {response.text}",
        )
        project = response.json()
        self.created_projects.append(project["id"])
        return project

    def create_category(self, title="Test Category", description=""):
        """Utility method to create a Category."""
        payload = {"title": title, "description": description}
        response = self.session.post(
            f"{self.BASE_URL}/categories", json=payload, headers=self.HEADERS_JSON
        )
        self.assertEqual(
            response.status_code,
            201,
            msg=f"Failed to create Category: {response.status_code} {response.text}",
        )
        category = response.json()
        self.created_categories.append(category["id"])
        return category

    def parse_xml(self, xml_str):
        """Utility method to parse XML response and return the root Element."""
        try:
            root = ET.fromstring(xml_str)
            return root
        except ET.ParseError:
            self.fail("Malformed XML received.")

    def send_xml_post(self, endpoint, xml_payload):
        """Utility method to send POST request with XML payload."""
        response = self.session.post(
            f"{self.BASE_URL}{endpoint}", data=xml_payload, headers=self.HEADERS_XML
        )
        return response

    def send_xml_put(self, endpoint, xml_payload):
        """Utility method to send PUT request with XML payload."""
        response = self.session.put(
            f"{self.BASE_URL}{endpoint}", data=xml_payload, headers=self.HEADERS_XML
        )
        return response
