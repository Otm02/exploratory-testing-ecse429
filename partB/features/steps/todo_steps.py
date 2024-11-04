from behave import given, when, then
import requests
from features.steps.utils import get_todo_by_title, get_all_todos, reset_database_to_default, get_all_projects, get_all_categories

BASE_URL = 'http://localhost:4567'


@given('the todo list application is running')
def step_impl(context):
    try:
        response = requests.get(f'{BASE_URL}')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        assert False, f"Service is not running: {e}"

@given('the database contains the default todo objects')
def step_impl(context):
    reset_database_to_default()
    context.default_todos = get_all_todos()
    context.default_projects = get_all_projects()
    context.default_categories = get_all_categories()

@when('a todo item with title "{title}" exists')
@given('a todo item with title "{title}" exists')
def step_impl(context, title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/todos', json=payload)
    assert response.status_code == 201, f"Failed to create todo item with title '{title}'"
    todo = response.json()
    context.todo_id = todo['id']
    add_to_todos_dict(context, title, todo['id'])

def add_to_todos_dict(context, key, value):
    if not hasattr(context, 'todosDict') or context.todosDict is None:
        context.todosDict = {}
    
    context.todosDict[key] = value

@when('I create a new todo with only title "{title}"')
def step_impl(context, title):
    payload = {'title': title}
    context.response = requests.post(f'{BASE_URL}/todos', json=payload)

@then('the todo item should be created with only title "{title}"')
def step_impl(context, title):
    assert context.response.status_code == 201, f"Expected status code 201, got {context.response.status_code}"
    todo = context.response.json()
    assert todo.get('title') == title, f"Expected title '{title}', got '{todo.get('title')}'"

@when('I create a new todo with title "{title}" and description "{description}"')
def step_impl(context, title, description):
    payload = {'title': title, 'description': description}
    context.response = requests.post(f'{BASE_URL}/todos', json=payload)

@then('the todo item should be created with title "{title}" and description "{description}"')
def step_impl(context, title, description):
    assert context.response.status_code == 201, f"Expected status code 201, got {context.response.status_code}"
    todo = context.response.json()
    assert todo.get('title') == title, f"Expected title '{title}', got '{todo.get('title')}'"
    assert todo.get('description') == description, f"Expected description '{description}', got '{todo.get('description')}'"

@when('I attempt to create a new todo without a title')
def step_impl(context):
    payload = {}
    context.response = requests.post(f'{BASE_URL}/todos', json=payload)

@then('the todo item should not be created')
def step_impl(context):
    assert context.response.status_code == 400, f"Expected error status code, got {context.response.status_code}"

@then('I should receive an error message "{error_message}" indicating the title field is mandatory')
def step_impl(context, error_message):
    assert 'errorMessages' in context.response.json(), "Expected error messages in response"
    error_messages = context.response.json()['errorMessages']
    expected_error = error_message
    assert expected_error in error_messages, f"Expected error message '{expected_error}', got '{error_messages}'"

@when('I update the description of the todo item with title "{title}" to "{description}"')
def step_impl(context, title, description):
    todo = get_todo_by_title(title)
    assert todo is not None, f"No todo item found with title '{title}'"
    todo_id = todo['id']
    payload = {'description': description}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}', json=payload)
    context.todo_id = todo_id

@then('the todo item should have description "{description}"')
def step_impl(context, description):
    todo_id = context.todo_id
    response = requests.get(f'{BASE_URL}/todos/{todo_id}')
    assert response.status_code == 200, f"Failed to retrieve todo item with id '{todo_id}'"
    todo = response.json()['todos'][0]
    assert todo.get('description') == description, f"Expected description '{description}', got '{todo.get('description')}'"

@when('I update the title of the todo item with title "{old_title}" to "{new_title}" and description to "{description}"')
def step_impl(context, old_title, new_title, description):
    todo = get_todo_by_title(old_title)
    assert todo is not None, f"No todo item found with title '{old_title}'"
    todo_id = todo['id']
    payload = {'title': new_title, 'description': description}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}', json=payload)
    context.todo_id = todo_id

@then('the todo item should have title "{title}" and description "{description}"')
def step_impl(context, title, description):
    todo_id = context.todo_id
    response = requests.get(f'{BASE_URL}/todos/{todo_id}')
    assert response.status_code == 200, f"Failed to retrieve todo item with id '{todo_id}'"
    todo = response.json()['todos'][0]
    assert todo.get('title') == title, f"Expected title '{title}', got '{todo.get('title')}'"
    assert todo.get('description') == description, f"Expected description '{description}', got '{todo.get('description')}'"

@when('I attempt to update the description of a todo item with id "{todo_id}" to "{description}"')
def step_impl(context, todo_id, description):
    payload = {'description': description}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}', json=payload)
    context.todo_id = todo_id

@then('I should receive an error message indicating the todo item does not exist')
def step_impl(context):
    assert context.response.status_code == 404, f"Expected status code 404, got {context.response.status_code}"
    assert 'errorMessages' in context.response.json(), "Expected error messages in response"

@when('I delete the todo item with title "{title}"')
def step_impl(context, title):
    todo = get_todo_by_title(title)
    assert todo is not None, f"No todo item found with title '{title}'"
    todo_id = todo['id']
    context.response = requests.delete(f'{BASE_URL}/todos/{todo_id}')
    context.todo_id = todo_id

@then('the todo item "{title}" should no longer exist')
def step_impl(context, title):
    todo = get_todo_by_title(title)
    assert todo is None, f"Todo item with title '{title}' still exists"

@when('I attempt to delete a todo item with id "{todo_id}"')
def step_impl(context, todo_id):
    context.response = requests.delete(f'{BASE_URL}/todos/{todo_id}')
    context.todo_id = todo_id

@given('the todo item with title "{todo_title}" is associated with the project "{project_title}" and category "{category_title}"')
def step_impl(context, todo_title, project_title, category_title):
    # Create project
    payload = {'title': project_title}
    response = requests.post(f'{BASE_URL}/projects', json=payload)
    assert response.status_code == 201, f"Failed to create project '{project_title}'"
    project = response.json()
    project_id = project['id']

    # Create category
    payload = {'title': category_title}
    response = requests.post(f'{BASE_URL}/categories', json=payload)
    assert response.status_code == 201, f"Failed to create category '{category_title}'"
    category = response.json()
    category_id = category['id']

    # Associate project with todo
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': project_id}
    response = requests.post(f'{BASE_URL}/todos/{todo_id}/tasksof', json=payload)
    assert response.status_code == 201, f"Failed to associate project with todo"

    # Associate category with todo
    payload = {'id': category_id}
    response = requests.post(f'{BASE_URL}/todos/{todo_id}/categories', json=payload)
    assert response.status_code == 201, f"Failed to associate category with todo"

@then('the associations should be removed')
def step_impl(context):
    todo_id = context.todo_id
    # Check projects
    response = requests.get(f'{BASE_URL}/todos/{todo_id}/tasksof')
    assert response.status_code == 404, "Expected 404 since todo should be deleted"
    # Check categories
    response = requests.get(f'{BASE_URL}/todos/{todo_id}/categories')
    assert response.status_code == 404, "Expected 404 since todo should be deleted"

@when('todo items with titles "{todo1}" "{todo2}" "{todo3}" exist and are associated to project')
def step_impl(context, todo1, todo2, todo3):
    context.todo_ids = []
    for todo in [todo1, todo2, todo3]:
        context.execute_steps(f'''
            Given a todo item with title "{todo}" exists
            When I add the todo to the project
        ''')
        