""" Custom admin site for the Explore Data Structure model
"""
from django.contrib import admin


class CustomExploreDataStructureAdmin(admin.ModelAdmin):
    """CustomExploreDataStructureAdmin"""

    readonly_fields = ["template", "data_structure_element_root"]
    exclude = ["selected_fields_html_tree"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Data Structures"""
        return False
