""" Discover rules for core explore example app
"""
from django.contrib.auth.models import Permission, Group
from core_main_app.permissions import rights as main_rights
from core_explore_example_app.permissions import rights as explore_example_rights


def init_permissions():
    """Initialization of groups and permissions

    Returns:

    """
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(name=main_rights.default_group)

        # Get explore example permissions
        explore_access_perm = Permission.objects.get(codename=explore_example_rights.explore_example_access)
        explore_save_query_perm = Permission.objects.get(codename=explore_example_rights.explore_example_save_query)
        explore_delete_query_perm = Permission.objects.get(codename=explore_example_rights.explore_example_delete_query)

        # add permissions to default group
        default_group.permissions.add(explore_access_perm,
                                      explore_save_query_perm,
                                      explore_delete_query_perm)
    except Exception, e:
        print('ERROR : Impossible to init the permissions : ' + e.message)
