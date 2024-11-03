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
    context.project_id = response.json()['id']

@when('I create a new project with all fields "{title}" "{completed}" "{active}" "{description}"')
def step_impl(context, title, completed, active, description):
    data = {"title": title, "completed": completed == "true", "active": active == "true", "description": description}
    response = requests.post(f"{BASE_URL}/projects", json=data)
    assert response.status_code == 201, f"Failed to create project"
    context.project_id = response.json().get('id')

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
    assert context.response.status_code == 404, f"Expected error status code, got {context.response.status_code}"
    assert 'errorMessages' in context.response.json(), "Expected error messages in response"

@when('I attempt to create a new project with fake field "{fake}"')
def step_impl(context, fake):
    data = {"fake": fake}
    response = requests.post(f"{BASE_URL}/projects", json=data)
    context.response = response.json()

@then('the project should be created with all fields "{title}" "{completed}" "{active}" "{description}"')
def step_impl(context, title, completed, active, description):    
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}")
    assert response.status_code == 200, f"Failed to retrieve project with id '{context.project_id}'"

    project = response.json().get('projects')[0]
    assert project.get('title') == title, f"Expected title '{title}', got {project.get('title')}"
    assert project.get('active') == active, f"Expected active '{active}', got '{project.get('active')}'"
    assert project.get('completed') == completed, f"Expected completed '{completed}', got '{project.get('completed')}'"
    assert project.get('description') == description, f"Expected description '{description}', got '{project.get('description')}'"

@then('the project should be created with "{title}"')
def step_impl(context, title):    
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}")
    assert response.status_code == 200, f"Failed to retrieve project with id '{context.project_id}'"

    project = response.json().get('projects')[0]
    assert project.get('title') == title, f"Expected title '{title}', got {project.get('title')}"

@then('the response should contain an error message indicating fake field')
def step_impl(context):
    assert context.response.get("errorMessages")[0] == "Could not find field: fake", "Unexpected error message"

@when('I replace the todo "{old_todo_title}" with "{new_todo_title}" in the project')
def step_impl(context, old_todo_title, new_todo_title):
    # Remove old todo
    old_todo_id = context.todosDict[old_todo_title]
    response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/tasks/{old_todo_id}")
    assert response.status_code == 200, f"Failed to remove old todo from project"
    # Add new todo
    new_todo_id = context.todosDict[new_todo_title]
    data = {"id": new_todo_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json=data)
    assert response.status_code == 201, f"Failed to add new todo to project"

@when('I update the project\'s todos to "{new_todo1}" and "{new_todo2}"')
def step_impl(context, new_todo1, new_todo2):
    # Remove all existing todos from the project
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get project's todos"
    todos = response.json().get('todos', [])
    for todo in todos:
        todo_id = todo.get('id')
        delete_response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/tasks/{todo_id}")
        assert delete_response.status_code == 200, f"Failed to remove todo {todo_id}"
    # Add new todos
    for todo_title in [new_todo1, new_todo2]:
        context.execute_steps(f'''
            Given a todo item with title "{todo_title}" exists
            When I add the todo to the project
        ''')

@when('I attempt to replace the todo "{existing_todo_title}" with non-existing todo id "{non_existing_todo_id}"')
def step_impl(context, existing_todo_title, non_existing_todo_id):
    # Remove existing todo
    existing_todo_id = context.todosDict[existing_todo_title]
    response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/tasks/{existing_todo_id}")
    assert response.status_code == 200, f"Failed to remove existing todo from project"
    # Attempt to add non-existing todo
    data = {"id": non_existing_todo_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json=data)
    context.response = response

@then('the project should contain the todo "{todo_title}"')
def step_impl(context, todo_title):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get todos of the project"
    todos = response.json().get('todos', [])
    todo_ids = [todo.get('id') for todo in todos]
    expected_todo_id = context.todosDict[todo_title]
    assert expected_todo_id in todo_ids, f"Todo {expected_todo_id} not found in project's tasks"

@then('the project should not contain the todo "{todo_title}"')
def step_impl(context, todo_title):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get todos of the project"
    todos = response.json().get('todos', [])
    todo_ids = [todo.get('id') for todo in todos]
    todo_id = context.todosDict[todo_title]
    assert todo_id not in todo_ids, f"Todo {todo_id} should not be in project's tasks"

@then('the project should contain the todos "{todo1}" and "{todo2}"')
def step_impl(context, todo1, todo2):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get todos of the project"
    todos = response.json().get('todos', [])
    todo_ids_in_project = [todo.get('id') for todo in todos]
    for todo_title in [todo1, todo2]:
        expected_todo_id = context.todosDict[todo_title]
        assert expected_todo_id in todo_ids_in_project, f"Todo {expected_todo_id} not found in project's tasks"

@then('the project should not contain the todos "{todo1}" and "{todo2}"')
def step_impl(context, todo1, todo2):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get todos of the project"
    todos = response.json().get('todos', [])
    todo_ids_in_project = [todo.get('id') for todo in todos]
    for todo_title in [todo1, todo2]:
        todo_id = context.todosDict[todo_title]
        assert todo_id not in todo_ids_in_project, f"Todo {todo_id} should not be in project's tasks"

@when('I add the todo to the project')
def step_impl(context):
    data = {"id": context.todo_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json=data)
    context.response = response
    assert response.status_code == 201, f"Failed to add todo to project"

@when('I add the todos to the project')
def step_impl(context):
    for todo_id in context.todo_ids:
        data = {"id": todo_id}
        response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json=data)
        assert response.status_code == 201, f"Failed to add todo {todo_id} to project"

@when('I attempt to add a non-existing todo with id "{todo_id}" to the project')
def step_impl(context, todo_id):
    data = {"id": todo_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json=data)
    context.response = response

@then('the project should contain the todo')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get tasks of the project"
    tasks = response.json().get('todos', [])
    todo_ids = [task.get('id') for task in tasks]
    assert context.todo_id in todo_ids, f"Todo {context.todo_id} not found in project's tasks"

@then('the project should contain the todos')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, "Failed to get tasks of the project"
    tasks = response.json().get('todos', [])
    task_ids = [task.get('id') for task in tasks]
    for todo_id in context.todo_ids:
        assert todo_id in task_ids, f"Todo {todo_id} not found in project's tasks"

@then('the response should contain an error message indicating the todo does not exist')
def step_impl(context):
    assert context.response.status_code == 404, f"Expected 404 Not Found, got {context.response.status_code}"
    error_messages = context.response.json().get("errorMessages", [])
    assert error_messages, "No error messages found in the response"
    actual_message = error_messages[0]
    assert "Could not find thing matching value for id" == actual_message, f"Unexpected error message: {actual_message}"

@when('I add the category to the project')
def step_impl(context):
    data = {"id": context.category_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", json=data)
    context.response = response
    assert response.status_code == 201, f"Failed to add category to project"

@when('I add the categories to the project')
def step_impl(context):
    for category_id in context.category_ids:
        data = {"id": category_id}
        response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", json=data)
        assert response.status_code == 201, f"Failed to add category {category_id} to project"

@when('I attempt to add a non-existing category with id "{category_id}" to the project')
def step_impl(context, category_id):
    data = {"id": category_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", json=data)
    context.response = response

@then('the project should contain the category')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids = [category.get('id') for category in categories]
    assert context.category_id in category_ids, f"Category {context.category_id} not found in project's categories"

@then('the project should contain the categories')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids_in_project = [category.get('id') for category in categories]
    for category_id in context.category_ids:
        assert category_id in category_ids_in_project, f"Category {category_id} not found in project's categories"

@then('the response should contain an error message indicating the category does not exist')
def step_impl(context):
    error_messages = context.response.json().get("errorMessages")
    actual_message = error_messages[0]
    assert "Could not find thing matching value for id" == actual_message, f"Unexpected error message: {actual_message}"

@given('I add the categories "{category1}" and "{category2}" to the project')
def step_impl(context, category1, category2):
    for category_title in [category1, category2]:
        context.execute_steps(f'''Given I add the category "{category_title}" to the project''')

@when('I replace the category "{old_category_title}" with "{new_category_title}" in the project')
def step_impl(context, old_category_title, new_category_title):
    # Remove old category
    old_category_id = context.categoryDict[old_category_title]
    response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/categories/{old_category_id}")
    assert response.status_code == 200, f"Failed to remove old category from project"
    # Add new category
    new_category_id = context.categoryDict[new_category_title]
    data = {"id": new_category_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", json=data)
    assert response.status_code == 201, f"Failed to add new category to project"

@when('I update the project\'s categories to "{new_category1}" and "{new_category2}"')
def step_impl(context, new_category1, new_category2):
    # Remove all existing categories from the project
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get project's categories"
    categories = response.json().get('categories', [])
    for category in categories:
        category_id = category.get('id')
        delete_response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/categories/{category_id}")
        assert delete_response.status_code == 200, f"Failed to remove category {category_id}"
    # Add new categories
    for category_title in [new_category1, new_category2]:
        context.execute_steps(f'''
            Given a category with title "{category_title}" exists
            When I add the category to the project
        ''')

@when('I attempt to replace the category "{existing_category_title}" with non-existing category id "{non_existing_category_id}"')
def step_impl(context, existing_category_title, non_existing_category_id):
    # Remove existing category
    existing_category_id = context.categoryDict[existing_category_title]
    response = requests.delete(f"{BASE_URL}/projects/{context.project_id}/categories/{existing_category_id}")
    assert response.status_code == 200, f"Failed to remove existing category from project"
    # Attempt to add non-existing category
    data = {"id": non_existing_category_id}
    response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", json=data)
    context.response = response

@then('the project should contain the category "{category_title}"')
def step_impl(context, category_title):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids = [category.get('id') for category in categories]
    expected_category_id = context.categoryDict[category_title]
    assert expected_category_id in category_ids, f"Category {expected_category_id} not found in project's categories"

@then('the project should not contain the category "{category_title}"')
def step_impl(context, category_title):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids = [category.get('id') for category in categories]
    category_id = context.categoryDict[category_title]
    assert category_id not in category_ids, f"Category {category_id} should not be in project's categories"

@then('the project should contain the categories "{category1}" and "{category2}"')
def step_impl(context, category1, category2):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids_in_project = [category.get('id') for category in categories]
    for category_title in [category1, category2]:
        expected_category_id = context.categoryDict[category_title]
        assert expected_category_id in category_ids_in_project, f"Category {expected_category_id} not found in project's categories"

@then('the project should not contain the categories "{category1}" and "{category2}"')
def step_impl(context, category1, category2):
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/categories")
    assert response.status_code == 200, "Failed to get categories of the project"
    categories = response.json().get('categories', [])
    category_ids_in_project = [category.get('id') for category in categories]
    for category_title in [category1, category2]:
        category_id = context.categoryDict[category_title]
        assert category_id not in category_ids_in_project, f"Category {category_id} should not be in project's categories"

@then('the project should still contain the category "{category_title}"')
def step_impl(context, category_title):
    context.execute_steps(f'''Then the project should contain the category "{category_title}"''')