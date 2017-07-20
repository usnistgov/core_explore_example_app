"""Explore example user views
"""
import json

import core_main_app.components.template_version_manager.api as template_version_manager_api
import core_main_app.utils.decorators as decorators
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_main_app.components.template import api as template_api
from core_main_app.utils.rendering import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.utils.decorators import method_decorator

import core_explore_example_app.permissions.rights as rights
from core_explore_example_app.components.saved_query import api as saved_query_api
from core_explore_example_app.settings import INSTALLED_APPS


class IndexView(View):
    api = template_version_manager_api
    get_redirect = 'core_explore_example_app/user/index.html'
    select_object_redirect = "core_explore_example_select_fields"
    object_name = "template"

    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_example_content_type,
                                          permission=rights.explore_example_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def get(self, request, *args, **kwargs):
        """ Page that allows to select a template to start exploring data

        Args:
            request:

        Returns:

        """
        assets = {
            "css": ['core_explore_example_app/user/css/style.css']
        }

        global_active_template_list = self.get_global_active_list()
        user_active_template_list = self.get_user_active_list(request.user.id)

        context = {
            'global_objects': global_active_template_list,
            'user_objects': user_active_template_list,
            'object_name': self.object_name,
            'select_object_redirect': self.select_object_redirect,
        }

        return render(request, self.get_redirect, assets=assets, context=context)

    def get_global_active_list(self):
        """ Get all global version managers.

        Args:

        Returns:
            List of all global version managers

        """
        return self.api.get_active_global_version_manager()

    def get_user_active_list(self, user_id):
        """ Get all active version managers with given user id.

        Args:
            user_id:

        Returns:
            List of all global version managers with given user.

        """
        return self.api.get_active_version_manager_by_user_id(user_id)


class SelectFieldsView(View):
    build_query_url = 'core_explore_example_build_query'

    # TODO: form generation can take time
    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_example_content_type,
                                          permission=rights.explore_example_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def get(self, request, template_id, *args, **kwargs):
        """Loads view to customize exploration tree

        Args:
            request:
            template_id:

        Returns:

        """
        try:
            # Set the assets
            assets = {
                "js": [
                    {
                        "path": 'core_main_app/common/js/XMLTree.js',
                        "is_raw": False
                    },
                    {
                        "path": "core_parser_app/js/autosave.js",
                        "is_raw": False
                    },
                    {
                        "path": "core_parser_app/js/autosave_checkbox.js",
                        "is_raw": False
                    },
                    {
                        "path": "core_parser_app/js/autosave.raw.js",
                        "is_raw": True
                    },
                    {
                        "path": "core_parser_app/js/choice.js",
                        "is_raw": False
                    },
                    {
                        "path": "core_explore_example_app/user/js/select_fields.js",
                        "is_raw": False
                    },
                    {
                        "path": "core_explore_example_app/user/js/select_fields.raw.js",
                        "is_raw": True
                    },
                ],
                "css": ['core_explore_example_app/user/css/xsd_form.css',
                        'core_explore_example_app/user/css/style.css']
            }

            # Set the context
            context = {
                "template_id": template_id,
                "build_query_url": self.build_query_url
            }

            return render(request,
                          'core_explore_example_app/user/select_fields.html',
                          assets=assets,
                          context=context)
        except Exception, e:
            return render(request,
                          'core_explore_example_app/user/errors.html',
                          assets={},
                          context={'errors': e.message})


class BuildQueryView(View):
    build_query_url = 'core_explore_example_build_query'
    get_query_url = 'core_explore_example_get_query'
    results_url = 'core_explore_example_results'
    object_name = "template"

    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_example_content_type,
                                          permission=rights.explore_example_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def get(self, request, template_id, query_id=None):
        """Page that allows to build and submit queries

        Args:
            request:
            template_id:
            query_id:

        Returns:

        """
        try:
            template = template_api.get(template_id)
            if template is None:
                return render(request,
                              'core_explore_example_app/user/errors.html',
                              assets={},
                              context={'errors': "The selected {0} does not exist".
                                       format(self.object_name)})

            # Init variables
            custom_form_string = ""
            saved_query_form = ""

            # If custom fields form present, set it
            if 'customFormStringExplore' in request.session:
                custom_form_string = request.session['customFormStringExplore']

            # If new form
            if query_id is None:
                # empty session variables
                request.session['mapCriteriaExplore'] = dict()
                request.session['savedQueryFormExplore'] = ""
                # create new query object
                query = self._create_new_query(request.user.id, template)
            else:
                # if not a new form and a query form is present in session
                if 'savedQueryFormExplore' in request.session:
                    saved_query_form = request.session['savedQueryFormExplore']
                query = query_api.get_by_id(query_id)

            # Get saved queries of a user
            if '_auth_user_id' in request.session:
                user_id = request.session['_auth_user_id']
                user_queries = saved_query_api.get_all_by_user_and_template(user_id=user_id,
                                                                            template_id=template_id)
            else:
                user_queries = []

            if custom_form_string != "":
                custom_form = custom_form_string
            else:
                custom_form = None

            assets = {
                "js": [
                    {
                        "path": 'core_explore_example_app/user/js/build_query.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_explore_example_app/user/js/build_query.raw.js',
                        "is_raw": True
                    },
                    {
                        "path": 'core_parser_app/js/autosave.raw.js',
                        "is_raw": True
                    },
                    {
                        "path": "core_parser_app/js/choice.js",
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/common/js/modals/error_page_modal.js',
                        "is_raw": True
                    }
                ],
                "css": ["core_explore_example_app/user/css/query_builder.css",
                        "core_explore_example_app/user/css/xsd_form.css"]
            }

            context = {
                'queries': user_queries,
                'template_id': template_id,

                'custom_form': custom_form,
                'query_form': saved_query_form,
                'query_id': str(query.id),

                "build_query_url": self.build_query_url,
                "results_url": self.results_url,
                "get_query_url": self.get_query_url
            }

            modals = [
                "core_explore_example_app/user/modals/custom_tree.html",
                "core_explore_example_app/user/modals/sub_elements_query_builder.html",
                "core_main_app/common/modals/error_page_modal.html",
                "core_explore_example_app/user/modals/delete_all_queries.html",
                "core_explore_example_app/user/modals/delete_query.html"
            ]

            return render(request,
                          'core_explore_example_app/user/build_query.html',
                          assets=assets,
                          context=context,
                          modals=modals)
        except Exception, e:
            return render(request,
                          'core_explore_example_app/user/errors.html',
                          assets={},
                          context={'errors': e.message})

    @staticmethod
    def _create_new_query(user_id, template):
        """ Create a new query
        Args:
            user_id:
            template:

        """
        # create new query object
        query = Query(user_id=str(user_id), templates=[template])
        return query_api.upsert(query)


class ResultQueryView(View):
    back_to_query_redirect = 'core_explore_example_build_query'

    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_example_content_type,
                                          permission=rights.explore_example_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def get(self, request, template_id, query_id):
        """Query results view

        Args:
            request:
            template_id:
            query_id:

        Returns:

        """
        context = {
            'template_id': template_id,
            'query_id': query_id,
            'exporter_app': False,
            'back_to_query_redirect': self.back_to_query_redirect
        }

        assets = {
            "js": [
                {
                    "path": 'core_explore_common_app/user/js/results.js',
                    "is_raw": False
                },
                {
                    "path": 'core_explore_common_app/user/js/results.raw.js',
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/common/js/XMLTree.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/modals/error_page_modal.js',
                    "is_raw": True
                }
            ],
            "css": ["core_explore_example_app/user/css/query_result.css",
                    "core_main_app/common/css/XMLTree.css",
                    "core_explore_common_app/user/css/results.css"],
        }

        modals = [
            "core_main_app/common/modals/error_page_modal.html"
        ]

        if 'core_exporters_app' in INSTALLED_APPS:
            # add all assets needed
            assets['js'].extend([{
                    "path": 'core_exporters_app/user/js/exporters/list/modals/list_exporters_selector.js',
                    "is_raw": False
                }])
            # add the modal
            modals.extend([
                "core_exporters_app/user/exporters/list/modals/list_exporters_selector.html"
            ])
            # the modal need all selected template
            query = query_api.get_by_id(query_id)

            context['exporter_app'] = True
            context['templates_list'] = json.dumps([str(template.id) for template in query.templates])

        return render(request,
                      'core_explore_example_app/user/results.html',
                      assets=assets,
                      modals=modals,
                      context=context)
