"""Saved query model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template


class SavedQuery(models.Model):
    """Represents a query saved by the user (Query by Example)"""

    user_id = models.CharField(blank=False, max_length=200)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    query = models.TextField(blank=False)
    displayed_query = models.TextField(blank=False)

    class Meta:
        """Meta"""

        verbose_name = "Saved Query"
        verbose_name_plural = "Saved Queries"

    @staticmethod
    def get_all():
        """Get all Saved Query.

        Args:

        Returns:

        """
        return SavedQuery.objects.all()

    @staticmethod
    def get_by_id(query_id):
        """Get a saved query

        Args:
            query_id:

        Returns:

        """
        try:
            return SavedQuery.objects.get(pk=query_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all_by_user_and_template(user_id, template_id):
        """Gets a saved query by user id and template id

        Args:
            user_id:
            template_id:

        Returns:

        """
        return SavedQuery.objects.filter(
            user_id=str(user_id), template=template_id
        )
