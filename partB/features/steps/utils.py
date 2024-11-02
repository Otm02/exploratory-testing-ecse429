import requests

BASE_URL = 'http://localhost:4567'

def get_todo_by_title(title):
    response = requests.get(f'{BASE_URL}/todos', params={'title': title})
    if response.status_code == 200:
        todos = response.json().get('todos', [])
        return todos[0] if todos else None
    return None

def get_project_by_title(title):
    response = requests.get(f'{BASE_URL}/projects', params={'title': title})
    if response.status_code == 200:
        projects = response.json().get('projects', [])
        return projects[0] if projects else None
    return None

def get_category_by_title(title):
    response = requests.get(f'{BASE_URL}/categories', params={'title': title})
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        return categories[0] if categories else None
    return None

def delete_all_todos():
    response = requests.get(f'{BASE_URL}/todos')
    if response.status_code == 200:
        todos = response.json().get('todos', [])
        for todo in todos:
            todo_id = todo.get('id')
            requests.delete(f'{BASE_URL}/todos/{todo_id}')

def delete_all_projects():
    response = requests.get(f'{BASE_URL}/projects')
    if response.status_code == 200:
        projects = response.json().get('projects', [])
        for project in projects:
            project_id = project.get('id')
            requests.delete(f'{BASE_URL}/projects/{project_id}')

def delete_all_categories():
    response = requests.get(f'{BASE_URL}/categories')
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        for category in categories:
            category_id = category.get('id')
            requests.delete(f'{BASE_URL}/categories/{category_id}')
