""" Custom admin site for the Saved Query
"""
from django.contrib import admin


class CustomSavedQueryAdmin(admin.ModelAdmin):
    """CustomSavedQueryAdmin"""

    readonly_fields = ["template", "query", "displayed_query"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Saved Queries"""
        return False
