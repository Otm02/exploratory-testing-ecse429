from features.steps.utils import reset_database_to_default
import random

def before_all(context):
    """Shuffle features before execution starts."""
    random.shuffle(context._runner.features)

def before_feature(context, feature):
    """Shuffle scenarios within each feature."""
    random.shuffle(feature.scenarios)

def after_feature(context, scenario):
    reset_database_to_default()
