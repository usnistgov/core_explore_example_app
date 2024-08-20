""" Url router for the explore example application
"""

from django.conf.urls import include
from django.urls import re_path

from core_explore_example_app.utils.mongo_query import fields_to_query
from core_explore_example_app.views.user import (
    views as user_views,
    ajax as user_ajax,
)

urlpatterns = [
    re_path(
        r"^$",
        user_views.IndexView.as_view(),
        name="core_explore_example_index",
    ),
    re_path(r"^rest/", include("core_explore_example_app.rest.urls")),
    re_path(
        r"^select-fields/(?P<template_id>\w+)$",
        user_views.SelectFieldsView.as_view(),
        name="core_explore_example_select_fields",
    ),
    re_path(
        r"^build-query/(?P<template_id>\w+)$",
        user_views.BuildQueryView.as_view(),
        name="core_explore_example_build_query",
    ),
    re_path(
        r"^build-query/(?P<template_id>\w+)/(?P<query_id>\w+)$",
        user_views.BuildQueryView.as_view(),
        name="core_explore_example_build_query",
    ),
    re_path(
        r"^results/(?P<template_id>\w+)/(?P<query_id>\w+)$",
        user_views.ResultQueryView.as_view(),
        name="core_explore_example_results",
    ),
    re_path(
        r"^save-fields$",
        user_ajax.save_fields,
        name="core_explore_example_save_fields",
    ),
    re_path(
        r"^generate-element/(?P<explore_data_structure_id>\w+)$",
        user_ajax.generate_element,
        name="core_explore_example_generate_element",
    ),
    re_path(
        r"^generate-choice/(?P<explore_data_structure_id>\w+)$",
        user_ajax.generate_choice,
        name="core_explore_example_generate_choice",
    ),
    re_path(
        r"^remove-element$",
        user_ajax.remove_element,
        name="core_explore_example_remove_element",
    ),
    re_path(
        r"^select-element$",
        user_ajax.select_element,
        name="core_explore_example_select_element",
    ),
    re_path(
        r"^update-user-input$",
        user_ajax.update_user_input,
        name="core_explore_example_update_user_input",
    ),
    re_path(
        r"^get-sub-elements-query-builder$",
        user_ajax.get_sub_elements_query_builder,
        name="core_explore_example_get_sub_elements_query_builder",
    ),
    re_path(
        r"^insert-sub-elements-query$",
        user_ajax.insert_sub_elements_query,
        name="core_explore_example_insert_sub_elements_query",
    ),
    re_path(
        r"^add-criteria$",
        user_ajax.add_criteria,
        name="core_explore_example_add_criteria",
    ),
    re_path(
        r"^save-query$",
        user_ajax.SaveQueryView.as_view(fields_to_query_func=fields_to_query),
        name="core_explore_example_save_query",
    ),
    re_path(
        r"^clear-criteria$",
        user_ajax.clear_criteria,
        name="core_explore_example_clear_criteria",
    ),
    re_path(
        r"^clear-queries$",
        user_ajax.clear_queries,
        name="core_explore_example_clear_queries",
    ),
    re_path(
        r"^delete-query$",
        user_ajax.delete_query,
        name="core_explore_example_delete_query",
    ),
    re_path(
        r"^add-query-criteria$",
        user_ajax.add_query_criteria,
        name="core_explore_example_add_query_criteria",
    ),
    re_path(
        r"^get-query$",
        user_ajax.GetQueryView.as_view(fields_to_query_func=fields_to_query),
        name="core_explore_example_get_query",
    ),
    re_path(
        r"^get-persistent-query-url$",
        user_ajax.CreatePersistentQueryExampleUrlView.as_view(),
        name="core_explore_example_get_persistent_query_url",
    ),
    re_path(
        r"^results-redirect",
        user_views.ResultQueryExampleRedirectView.as_view(),
        name="core_explore_example_results_redirect",
    ),
]
