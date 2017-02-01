""" Explore data Structure api
"""
from core_explore_example_app.components.explore_data_structure.models import ExploreDataStructure


def get_by_user_id_and_template_id(user_id, template_id):
    """ Returns object with the given user id and template id

    Args:
        user_id:
        template_id:

    Returns:

    """
    return ExploreDataStructure.get_by_user_id_and_template_id(user_id, template_id)


def upsert(explore_data_structure):
    """Saves explore data structure

    Args:
        explore_data_structure:

    Returns:

    """
    return explore_data_structure.save()
