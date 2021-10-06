"""Url router for the administration site
"""
from django.contrib import admin

from core_explore_example_app.components.explore_data_structure.models import (
    ExploreDataStructure,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from core_main_app.admin import core_admin_site

admin_urls = []


admin.site.register(ExploreDataStructure)
admin.site.register(PersistentQueryExample)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
