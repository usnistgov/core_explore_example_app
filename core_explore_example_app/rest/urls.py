""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_explore_example_app.rest.saved_query import views as saved_query_views

urlpatterns = [
    re_path(r'^saved/query/$', saved_query_views.SavedQueryList.as_view(),
            name='core_explore_example_app_rest_saved_query_list'),

    re_path(r'^saved/query/(?P<pk>\w+)/$', saved_query_views.SavedQueryDetail.as_view(),
            name='core_explore_example_app_rest_saved_query_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
