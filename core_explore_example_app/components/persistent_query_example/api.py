""" Persistent Query Example API
"""
from core_main_app.access_control.api import has_perm_administration
from core_main_app.access_control.decorators import access_control
from core_explore_common_app.access_control.api import (
    can_read_persistent_query,
    can_write_persistent_query,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)


@access_control(can_write_persistent_query)
def upsert(persistent_query_example, user):
    """Saves or update persistent query

    Args:
        persistent_query_example:
        user:

    Returns:

    """
    persistent_query_example.save()
    return persistent_query_example


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
    """Return the Persistent Query Example with the given name

    Args:
        persistent_query_example_name:
        user:
    Returns:

    """
    return PersistentQueryExample.get_by_name(persistent_query_example_name)


@access_control(can_write_persistent_query)
def delete(persistent_query_example, user):
    """Deletes the Persistent Query Example and the element associated

    Args:
        persistent_query_example:
        user:
    """
    persistent_query_example.delete()


@access_control(can_write_persistent_query)
def set_name(persistent_query_example, name, user):
    """Set name to Persistent Query Example

    Args:
        persistent_query_example:
        name:
        user:
    """
    persistent_query_example.name = name
    persistent_query_example.save()


@access_control(has_perm_administration)
def get_all(user):
    """get all Persistent Query Example

    Args:
        user:
    """
    return PersistentQueryExample.get_all()


@access_control(can_read_persistent_query)
def get_all_by_user(user):
    """get persistent Query Example by user

    Args:
        user:
    """
    return PersistentQueryExample.get_all_by_user(user.id)
