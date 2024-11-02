from features.steps.utils import reset_database_to_default

def after_scenario(context, scenario):
    reset_database_to_default()
