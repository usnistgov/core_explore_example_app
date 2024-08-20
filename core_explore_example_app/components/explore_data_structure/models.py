"""Explore Data Structure
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions as exceptions
from core_parser_app.components.data_structure.models import DataStructure
from core_explore_example_app.permissions import rights


class ExploreDataStructure(DataStructure):
    """Explore data structure"""

    selected_fields_html_tree = models.TextField(
        blank=True, default=None, null=True
    )

    @staticmethod
    def get_permission():
        """Return permission

        Returns:

        """
        return f"{rights.EXPLORE_EXAMPLE_CONTENT_TYPE}.{rights.EXPLORE_EXAMPLE_DATA_STRUCTURE_ACCESS}"

    @staticmethod
    def get_by_user_id_and_template_id(user_id, template_id):
        """Return explore data structure given its id and template id

        Returns:

        """
        try:
            return ExploreDataStructure.objects.get(
                user=str(user_id), template=str(template_id)
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_id(data_structure_id):
        """Return the object with the given id.

        Args:
            data_structure_id:

        Returns:
            Explore Data Structure (obj): ExploreDataStructure object with the given id

        """
        try:
            return ExploreDataStructure.objects.get(pk=str(data_structure_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
