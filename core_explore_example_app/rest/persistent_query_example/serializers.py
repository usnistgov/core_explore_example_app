""" Serializers used for the persistent query example REST API.
"""
from rest_framework.serializers import ModelSerializer

from core_explore_example_app.components.persistent_query_example import (
    api as persistent_query_example_api,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)


class PersistentQueryExampleSerializer(ModelSerializer):
    """Persistent query example"""

    class Meta:
        """Meta"""

        model = PersistentQueryExample
        fields = ["id", "user_id", "content", "templates", "name"]
        read_only_fields = ("id", "user_id")

    def create(self, validated_data):
        """Create and return a new `PersistentQueryExample` instance, given the validated data."""

        # Create instance from the validated data and insert it in DB
        persistent_query_example = PersistentQueryExample(
            user_id=str(self.context["request"].user.id),
            content=validated_data["content"]
            if "content" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )

        if "templates" in validated_data:
            persistent_query_example.templates.set(validated_data["templates"])
        return persistent_query_example

    # Update instance from the validated data and insert it in DB
    def update(self, persistent_query_example, validated_data):
        """Update and return an existing `PersistentQueryExample` instance, given the validated
        data.
        """
        persistent_query_example.content = validated_data.get(
            "content", persistent_query_example.content
        )
        persistent_query_example.name = validated_data.get(
            "name", persistent_query_example.name
        )
        persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )
        if "templates" in validated_data:
            persistent_query_example.templates.set(validated_data["templates"])
        return persistent_query_example


class PersistentQueryExampleAdminSerializer(ModelSerializer):
    """PersistentQueryAdminExample Serializer"""

    class Meta:
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
            content=validated_data["content"]
            if "content" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        persistent_query_example_api.upsert(
            persistent_query_example, self.context["request"].user
        )
        if "templates" in validated_data:
            persistent_query_example.templates.set(validated_data["templates"])
        return persistent_query_example
