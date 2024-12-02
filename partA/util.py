import requests

BASE_URL = 'http://localhost:4567'
session = requests.Session()

def create_todo(title="Test TODO"*100000, doneStatus=False, description="Description"*100000):
    response = session.post(f"{BASE_URL}/todos", json={"title": title, "doneStatus": doneStatus, "description": description})
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status: {response.status_code}, Response: {response.text}")
    return response.json()["id"]

def delete_todo(todo_id):
    response = session.delete(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code != 200:
        raise Exception(f"Failed to delete todo {todo_id}. Status: {response.status_code}, Response: {response.text}")

def post_on_todos_id(todo_id, project_ids):
    for project_id in project_ids:
        response = session.post(f"{BASE_URL}/todos/{todo_id}/tasksof", json={"id": project_id})
        if response.status_code != 201:
            raise Exception(f"Failed to connect todo {todo_id} with project {project_id}. Status: {response.status_code}, Response: {response.text}")

def create_project(title="Test Project"*100000, completed=False, active=True, description="Decription"*100000):
    response = session.post(f"{BASE_URL}/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    if response.status_code != 201:
        raise Exception(f"Failed to create project. Status: {response.status_code}, Response: {response.text}")
    return response.json()["id"]

def delete_project(project_id):
    response = session.delete(f"{BASE_URL}/projects/{project_id}")
    if response.status_code != 200:
        raise Exception(f"Failed to delete project {project_id}. Status: {response.status_code}, Response: {response.text}")

def post_on_projects_id(project_id, todo_ids):
    for todo_id in todo_ids:
        response = session.post(f"{BASE_URL}/projects/{project_id}/tasks", json={"id": todo_id})
        if response.status_code != 201:
            raise Exception(f"Failed to connect project {project_id} with todo {todo_id}. Status: {response.status_code}, Response: {response.text}")