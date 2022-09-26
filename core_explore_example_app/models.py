"""Explore Example models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_explore_example_app.permissions import rights


class ExploreExample(models.Model):
    """Explore Example"""

    class Meta:
        """Meta"""

        verbose_name = "core_explore_example_app"
        default_permissions = ()
        permissions = (
            (
                rights.EXPLORE_EXAMPLE_ACCESS,
                get_formatted_name(rights.EXPLORE_EXAMPLE_ACCESS),
            ),
            (
                rights.EXPLORE_EXAMPLE_SAVE_QUERY,
                get_formatted_name(rights.EXPLORE_EXAMPLE_SAVE_QUERY),
            ),
            (
                rights.EXPLORE_EXAMPLE_DELETE_QUERY,
                get_formatted_name(rights.EXPLORE_EXAMPLE_DELETE_QUERY),
            ),
            (
                rights.EXPLORE_EXAMPLE_DATA_STRUCTURE_ACCESS,
                get_formatted_name(
                    rights.EXPLORE_EXAMPLE_DATA_STRUCTURE_ACCESS
                ),
            ),
        )
