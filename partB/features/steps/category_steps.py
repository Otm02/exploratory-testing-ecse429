from behave import given, when, then
import requests
from features.steps.utils import get_category_by_title, get_todo_by_title

BASE_URL = 'http://localhost:4567'

def get_category_by_title(title):
    response = requests.get(f'{BASE_URL}/categories', params={'title': title})
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        return categories[0] if categories else None
    return None

@given('a category with title "{title}" exists')
def step_impl(context, title):
    payload = {'title': title}
    response = requests.post(f'{BASE_URL}/categories', json=payload)
    assert response.status_code == 201, f"Failed to create category with title '{title}'"
    category = response.json()
    context.category_id = category['id']
    add_to_category_dict(context, title, category.get('id'))

def add_to_category_dict(context, key, value):
    if not hasattr(context, 'categoryDict') or context.categoryDict is None:
        context.categoryDict = {}
    
    context.categoryDict[key] = value

@given('I have categories with titles "{category1}" "{category2}"')
def step_impl(context, category1, category2):
    for category_title in [category1, category2]:
        context.execute_steps(f'''Given I create a category with title "{category_title}"''')

@when('I associate the category "{category_title}" with the todo item "{todo_title}"')
def step_impl(context, category_title, todo_title):
    category = get_category_by_title(category_title)
    assert category is not None, f"No category found with title '{category_title}'"
    category_id = category['id']
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': category_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/categories', json=payload)

@then('the todo item "{todo_title}" should be associated with the category "{category_title}"')
def step_impl(context, todo_title, category_title):
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    response = requests.get(f'{BASE_URL}/todos/{todo_id}/categories')
    assert response.status_code == 200, f"Failed to retrieve categories for todo '{todo_title}'"
    categories = response.json().get('categories', [])
    titles = [cat.get('title') for cat in categories]
    assert category_title in titles, f"Category '{category_title}' not associated with todo '{todo_title}'"

@when('I create a category with title "{category_title}" and associate it with the todo item "{todo_title}"')
def step_impl(context, category_title, todo_title):
    payload = {'title': category_title}
    response = requests.post(f'{BASE_URL}/categories', json=payload)
    assert response.status_code == 201, f"Failed to create category with title '{category_title}'"
    category = response.json()
    category_id = category['id']
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': category_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/categories', json=payload)

@when('I attempt to associate a non-existent category with id "{category_id}" with the todo item "{todo_title}"')
def step_impl(context, category_id, todo_title):
    todo = get_todo_by_title(todo_title)
    assert todo is not None, f"No todo item found with title '{todo_title}'"
    todo_id = todo['id']
    payload = {'id': category_id}
    context.response = requests.post(f'{BASE_URL}/todos/{todo_id}/categories', json=payload)

@then('I should receive an error message indicating the category does not exist')
def step_impl(context):
    assert context.response.status_code == 404, f"Expected error status code, got {context.response.status_code}"
    assert 'errorMessages' in context.response.json(), "Expected error messages in response"

@when('I have categories with titles "{category1}" "{category2}" "{category3}"')
def step_impl(context, category1, category2, category3):
    context.category_ids = []
    for category_title in [category1, category2, category3]:
        data = {"title": category_title}
        response = requests.post(f"{BASE_URL}/categories", json=data)
        assert response.status_code == 201, f"Failed to create category '{category_title}'"
        category = response.json()
        category_id = category.get('id')
        context.category_ids.append(category_id)
