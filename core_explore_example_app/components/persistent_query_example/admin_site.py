""" Custom admin site for the Persistent Query Example model
"""
from django.contrib import admin


class CustomPersistentQueryExampleAdmin(admin.ModelAdmin):
    """CustomPersistentQueryExampleAdmin"""

    exclude = ["data_sources"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Persistent Queries"""
        return False
