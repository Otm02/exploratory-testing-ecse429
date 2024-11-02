import requests

BASE_URL = 'http://localhost:4567'

def reset_database_to_default():
    # Delete all existing data
    delete_all_todos()
    delete_all_projects()
    delete_all_categories()

    # Re-create default data
    # Create categories
    office_category = create_category("Office")
    home_category = create_category("Home")

    # Create todos
    paperwork_todo = create_todo("scan paperwork")
    filework_todo = create_todo("file paperwork")

    # Create project
    office_work_project = create_project("Office Work")

    # Associate todos with project
    associate_todo_with_project(paperwork_todo['id'], office_work_project['id'])
    associate_todo_with_project(filework_todo['id'], office_work_project['id'])

    # Associate todo with category
    associate_todo_with_category(paperwork_todo['id'], office_category['id'])

def create_todo(title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/todos', json=payload)
    response.raise_for_status()
    return response.json()

def create_project(title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/projects', json=payload)
    response.raise_for_status()
    return response.json()

def create_category(title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/categories', json=payload)
    response.raise_for_status()
    return response.json()

def associate_todo_with_project(todo_id, project_id):
    payload = {'id': project_id}
    response = requests.post(f'{BASE_URL}/todos/{todo_id}/tasksof', json=payload)
    response.raise_for_status()

def associate_todo_with_category(todo_id, category_id):
    payload = {'id': category_id}
    response = requests.post(f'{BASE_URL}/todos/{todo_id}/categories', json=payload)
    response.raise_for_status()

def get_all_todos():
    response = requests.get(f'{BASE_URL}/todos')
    response.raise_for_status()
    return response.json().get('todos', [])

def get_all_projects():
    response = requests.get(f'{BASE_URL}/projects')
    response.raise_for_status()
    return response.json().get('projects', [])

def get_all_categories():
    response = requests.get(f'{BASE_URL}/categories')
    response.raise_for_status()
    return response.json().get('categories', [])

def get_todo_by_title(title):
    response = requests.get(f'{BASE_URL}/todos')
    if response.status_code == 200:
        todos = response.json().get('todos', [])
        for todo in todos:
            if todo.get('title') == title:
                return todo
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
