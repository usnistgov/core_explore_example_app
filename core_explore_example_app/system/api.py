""" System API
"""
from core_explore_example_app.apps import ExploreExampleAppConfig
from core_explore_example_app.components.saved_query.models import SavedQuery


def get_saved_queries_created_by_app():
    """Return saved queries created by the app.

    Returns:

    """
    return SavedQuery.objects.filter(user_id=ExploreExampleAppConfig.name).all()
