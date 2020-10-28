""" Persistent Query Example API
"""
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from core_main_app.access_control.decorators import access_control
from core_explore_common_app.access_control.api import can_read_persistent_query


@access_control(can_read_persistent_query)
def get_by_id(persistent_query_example_id, user):
    """Return the Persistent Query Example with the given id

    Args:
        persistent_query_example_id:
        user:

    Returns:

    """
    return PersistentQueryExample.get_by_id(persistent_query_example_id)


@access_control(can_read_persistent_query)
def get_by_name(persistent_query_example_name, user):
    """Return the Persistent Query Keyword with the given name

    Args:
        persistent_query_example_name:
        user:
    Returns:

    """
    return PersistentQueryExample.get_by_name(persistent_query_example_name)
