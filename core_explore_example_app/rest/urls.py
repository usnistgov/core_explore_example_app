""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_explore_example_app.rest.persistent_query_example import (
    views as persistent_query_example_views,
)
from core_explore_example_app.rest.saved_query import (
    views as saved_query_views,
)

urlpatterns = [
    re_path(
        r"^saved/query/$",
        saved_query_views.SavedQueryList.as_view(),
        name="core_explore_example_app_rest_saved_query_list",
    ),
    re_path(
        r"^saved/query/(?P<pk>\w+)/$",
        saved_query_views.SavedQueryDetail.as_view(),
        name="core_explore_example_app_rest_saved_query_detail",
    ),
    re_path(
        r"^admin/persistent_query_example/$",
        persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
        name="core_explore_example_app_rest_persistent_query_example_admin_list",
    ),
    re_path(
        r"^persistent_query_example/$",
        persistent_query_example_views.PersistentQueryExampleList.as_view(),
        name="core_explore_example_app_rest_persistent_query_example_list",
    ),
    re_path(
        r"^persistent_query_example/(?P<pk>\w+)/$",
        persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
        name="core_explore_example_app_rest_persistent_query_example_detail",
    ),
    re_path(
        r"^persistent_query_example/name/(?P<name>\w+)/$",
        persistent_query_example_views.PersistentQueryExampleByName.as_view(),
        name="core_explore_example_app_rest_persistent_query_example_name",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
