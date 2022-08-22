"""Url router for the administration site
"""
from django.contrib import admin

from core_main_app.admin import core_admin_site
from core_explore_example_app.components.explore_data_structure.models import (
    ExploreDataStructure,
)
from core_explore_example_app.components.persistent_query_example.admin_site import (
    CustomPersistentQueryExampleAdmin,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from core_explore_example_app.components.saved_query.admin_site import (
    CustomSavedQueryAdmin,
)
from core_explore_example_app.components.explore_data_structure.admin_site import (
    CustomExploreDataStructureAdmin,
)
from core_explore_example_app.components.saved_query.models import SavedQuery

admin_urls = []


admin.site.register(ExploreDataStructure, CustomExploreDataStructureAdmin)
admin.site.register(PersistentQueryExample, CustomPersistentQueryExampleAdmin)
admin.site.register(SavedQuery, CustomSavedQueryAdmin)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
