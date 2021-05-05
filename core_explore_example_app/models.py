"""Explore Example models
"""

from django.db import models

from core_explore_example_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name


class ExploreExample(models.Model):
    class Meta(object):
        verbose_name = "core_explore_example_app"
        default_permissions = ()
        permissions = (
            (
                rights.explore_example_access,
                get_formatted_name(rights.explore_example_access),
            ),
            (
                rights.explore_example_save_query,
                get_formatted_name(rights.explore_example_save_query),
            ),
            (
                rights.explore_example_delete_query,
                get_formatted_name(rights.explore_example_delete_query),
            ),
            (
                rights.explore_example_data_structure_access,
                get_formatted_name(rights.explore_example_data_structure_access),
            ),
        )
