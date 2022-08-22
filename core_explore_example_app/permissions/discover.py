""" Discover rules for core explore example app.
"""
import logging

from core_main_app.permissions import rights as main_rights
from core_explore_example_app.permissions import rights as explore_example_rights

logger = logging.getLogger(__name__)


def init_permissions(apps):
    """Initialization of groups and permissions.

    Args:
        apps (Apps): List of applications to init
    """
    try:
        group = apps.get_model("auth", "Group")
        permission = apps.get_model("auth", "Permission")

        # Get or Create the default group
        default_group, created = group.objects.get_or_create(
            name=main_rights.DEFAULT_GROUP
        )

        # Get explore example permissions
        explore_access_perm = permission.objects.get(
            codename=explore_example_rights.EXPLORE_EXAMPLE_ACCESS
        )
        explore_save_query_perm = permission.objects.get(
            codename=explore_example_rights.EXPLORE_EXAMPLE_SAVE_QUERY
        )
        explore_delete_query_perm = permission.objects.get(
            codename=explore_example_rights.EXPLORE_EXAMPLE_DELETE_QUERY
        )
        explore_example_data_structure_access_perm = permission.objects.get(
            codename=explore_example_rights.EXPLORE_EXAMPLE_DATA_STRUCTURE_ACCESS
        )

        # Add permissions to default group
        default_group.permissions.add(
            explore_access_perm,
            explore_save_query_perm,
            explore_delete_query_perm,
            explore_example_data_structure_access_perm,
        )
    except Exception as exception:
        logger.error(
            "Impossible to init explore_example permissions: %s", str(exception)
        )
