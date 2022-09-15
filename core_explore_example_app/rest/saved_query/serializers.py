""" Saved Query Serializers
"""
from rest_framework.serializers import ModelSerializer

from core_explore_example_app.components.saved_query.models import SavedQuery


class SavedQuerySerializer(ModelSerializer):
    """Saved Query serializer"""

    class Meta:
        """Meta"""

        model = SavedQuery
        fields = "__all__"
        read_only_fields = ("user_id", "displayed_query")
