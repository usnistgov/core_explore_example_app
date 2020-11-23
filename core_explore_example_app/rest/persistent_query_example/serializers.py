""" Serializers used for the persistent query example REST API.
"""
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_explore_example_app.components.persistent_query_example import (
    api as persistent_query_example_api,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)


class PersistentQueryExampleSerializer(DocumentSerializer):
    """Persistent query example"""

    class Meta(object):
        model = PersistentQueryExample
        fields = ["id", "user_id", "content", "templates", "name"]
        read_only_fields = ("id", "user_id")

    def create(self, validated_data):
        """Create and return a new `PersistentQueryExample` instance, given the validated data."""

        # Create instance from the validated data and insert it in DB
        persistent_query_example = PersistentQueryExample(
            user_id=str(self.context["request"].user.id),
            content=validated_data["content"] if "content" in validated_data else None,
            templates=validated_data["templates"]
            if "templates" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        return persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )

    # Update instance from the validated data and insert it in DB
    def update(self, persistent_query_example, validated_data):
        """Update and return an existing `PersistentQueryExample` instance, given the validated
        data.
        """
        persistent_query_example.content = validated_data.get(
            "content", persistent_query_example.content
        )
        persistent_query_example.templates = validated_data.get(
            "templates", persistent_query_example.templates
        )
        persistent_query_example.name = validated_data.get(
            "name", persistent_query_example.name
        )
        return persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )


class PersistentQueryExampleAdminSerializer(DocumentSerializer):
    """PersistentQueryAdminExample Serializer"""

    class Meta(object):
        """Meta"""

        model = PersistentQueryExample
        fields = ["id", "user_id", "content", "templates", "name"]

    def create(self, validated_data):
        """
        Create and return a new `PersistentQueryExample` instance, given the validated data.
        """
        # Create data
        persistent_query_example = PersistentQueryExample(
            user_id=validated_data["user_id"],
            content=validated_data["content"] if "content" in validated_data else None,
            templates=validated_data["templates"]
            if "templates" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        return persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )
