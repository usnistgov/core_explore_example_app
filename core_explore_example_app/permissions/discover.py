""" Discover rules for core explore example app.
"""
import logging

from core_explore_example_app.permissions import rights as explore_example_rights
from core_main_app.permissions import rights as main_rights

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
            name=main_rights.default_group
        )

        # Get explore example permissions
        explore_access_perm = permission.objects.get(
            codename=explore_example_rights.explore_example_access
        )
        explore_save_query_perm = permission.objects.get(
            codename=explore_example_rights.explore_example_save_query
        )
        explore_delete_query_perm = permission.objects.get(
            codename=explore_example_rights.explore_example_delete_query
        )
        explore_example_data_structure_access_perm = permission.objects.get(
            codename=explore_example_rights.explore_example_data_structure_access
        )

        # Add permissions to default group
        default_group.permissions.add(
            explore_access_perm,
            explore_save_query_perm,
            explore_delete_query_perm,
            explore_example_data_structure_access_perm,
        )
    except Exception as e:
        logger.error("Impossible to init explore_example permissions: %s" % str(e))
