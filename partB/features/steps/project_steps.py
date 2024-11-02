from behave import given, when, then
import requests
from features.steps.utils import get_project_by_title, get_todo_by_title

BASE_URL = 'http://localhost:4567'

def get_project_by_title(title):
    response = requests.get(f'{BASE_URL}/projects', params={'title': title})
    if response.status_code == 200:
        projects = response.json().get('projects', [])
        return projects[0] if projects else None
    return None

@given('a project with title "{title}" exists')
def step_impl(context, title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/projects', json=payload)
    assert response.status_code == 201, f"Failed to create project with title '{title}'"
    project = response.json()
    context.project_id = project['id']

@when('I associate the project "{project_title}" with the todo item "{todo_title}"')
def step_impl(context, project_title, todo_title):
    project = get_project_by_title(project_title)
    assert project is not None, f"No project found with title '{project_title}'"
    project_id = project['id']
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': project_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/tasksof', json=payload)

@then('the todo item "{todo_title}" should be associated with the project "{project_title}"')
def step_impl(context, todo_title, project_title):
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    response = requests.get(f'{BASE_URL}/todos/{todo_id}/tasksof')
    assert response.status_code == 200, f"Failed to retrieve projects for todo '{todo_title}'"
    projects = response.json().get('projects', [])
    titles = [proj.get('title') for proj in projects]
    assert project_title in titles, f"Project '{project_title}' not associated with todo '{todo_title}'"

@when('I create a project with title "{project_title}" and associate it with the todo item "{todo_title}"')
def step_impl(context, project_title, todo_title):
    payload = {'title': project_title}
    response = requests.post(f'{BASE_URL}/projects', json=payload)
    assert response.status_code == 201, f"Failed to create project with title '{project_title}'"
    project = response.json()
    project_id = project['id']
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': project_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/tasksof', json=payload)

@when('I attempt to associate a non-existent project with id "{project_id}" with the todo item "{todo_title}"')
def step_impl(context, project_id, todo_title):
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': project_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/tasksof', json=payload)

@then('I should receive an error message indicating the project does not exist')
def step_impl(context):
    assert context.response.status_code in [404, 400], f"Expected error status code, got {context.response.status_code}"
    assert 'errorMessages' in context.response.json(), "Expected error messages in response"
