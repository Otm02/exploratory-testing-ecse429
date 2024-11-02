from features.steps.utils import delete_all_todos, delete_all_projects, delete_all_categories

def after_scenario(context, scenario):
    delete_all_todos()
    delete_all_projects()
    delete_all_categories()
