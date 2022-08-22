"""Explore example user views
"""
import json

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.settings import DATA_SORTING_FIELDS
import core_main_app.utils.decorators as decorators
from core_main_app.utils.rendering import render

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.settings import DEFAULT_DATE_TOGGLE_VALUE
from core_explore_common_app.views.user.views import (
    ResultQueryRedirectView,
    ResultsView,
)
from core_explore_example_app.permissions import rights
from core_explore_example_app.components.explore_data_structure import (
    api as explore_data_structure_api,
)
from core_explore_example_app.components.persistent_query_example import (
    api as persistent_query_example_api,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from core_explore_example_app.components.saved_query import api as saved_query_api
from core_explore_example_app.settings import INSTALLED_APPS
from core_explore_example_app.utils.parser import render_form


class IndexView(View):
    """Index View"""

    api = template_version_manager_api
    get_redirect = "core_explore_example_app/user/index.html"
    select_object_redirect = "core_explore_example_select_fields"
    build_query_redirect = "core_explore_example_build_query"
    object_name = "template"

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_EXAMPLE_CONTENT_TYPE,
            permission=rights.EXPLORE_EXAMPLE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, *args, **kwargs):
        """Page that allows to select a template to start exploring data

        Args:
            request:

        Returns:

        """
        assets = {"css": ["core_explore_example_app/user/css/style.css"]}

        global_active_template_list = self.get_global_active_list(request=request)
        user_active_template_list = self.get_user_active_list(request=request)

        context = {
            "global_objects": global_active_template_list,
            "user_objects": user_active_template_list,
            "object_name": self.object_name,
            "select_object_redirect": self.select_object_redirect,
            "build_query_redirect": self.build_query_redirect,
        }

        return render(request, self.get_redirect, assets=assets, context=context)

    def get_global_active_list(self, request):
        """Get all global version managers.

        Args:
            request:

        Returns:
            List of all global version managers

        """
        return self.api.get_active_global_version_manager(request=request)

    def get_user_active_list(self, request):
        """Get all active version managers with given user id.

        Args:
            request:

        Returns:
            List of all global version managers with given user.

        """
        return self.api.get_active_version_manager_by_user_id(request=request)


class SelectFieldsView(View):
    """Select Fields View"""

    build_query_url = "core_explore_example_build_query"
    load_form_url = "core_explore_example_load_form"
    generate_element_url = "core_explore_example_generate_element"
    remove_element_url = "core_explore_example_remove_element"
    generate_choice_url = "core_explore_example_generate_choice"

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_EXAMPLE_CONTENT_TYPE,
            permission=rights.EXPLORE_EXAMPLE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
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
                    {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                    {"path": "core_parser_app/js/autosave.js", "is_raw": False},
                    {
                        "path": "core_parser_app/js/autosave_checkbox.js",
                        "is_raw": False,
                    },
                    {"path": "core_parser_app/js/autosave.raw.js", "is_raw": True},
                    {"path": "core_parser_app/js/buttons.js", "is_raw": False},
                    {
                        "path": "core_explore_example_app/user/js/buttons.raw.js",
                        "is_raw": True,
                    },
                    {"path": "core_parser_app/js/modules.js", "is_raw": False},
                    {"path": "core_parser_app/js/choice.js", "is_raw": False},
                    {
                        "path": "core_explore_example_app/user/js/choice.raw.js",
                        "is_raw": True,
                    },
                    {
                        "path": "core_explore_example_app/user/js/select_fields.js",
                        "is_raw": False,
                    },
                    {
                        "path": "core_explore_example_app/user/js/select_fields.raw.js",
                        "is_raw": True,
                    },
                ],
                "css": [
                    "core_explore_example_app/user/css/xsd_form.css",
                    "core_explore_example_app/user/css/style.css",
                ],
            }

            template = template_api.get_by_id(template_id, request=request)
            # get data structure
            data_structure = (
                explore_data_structure_api.create_and_get_explore_data_structure(
                    template, request
                )
            )
            root_element = data_structure.data_structure_element_root

            # renders the form
            xsd_form = render_form(request, root_element)

            # Set the context
            context = {
                "template_id": template_id,
                "build_query_url": self.build_query_url,
                "load_form_url": self.load_form_url,
                "generate_element_url": self.generate_element_url,
                "remove_element_url": self.remove_element_url,
                "generate_choice_url": self.generate_choice_url,
                "data_structure_id": str(data_structure.id),
                "xsd_form": xsd_form,
            }

            return render(
                request,
                "core_explore_example_app/user/select_fields.html",
                assets=assets,
                context=context,
            )
        except Exception as exception:
            return render(
                request,
                "core_explore_example_app/user/errors.html",
                assets={},
                context={"errors": str(exception)},
            )


class BuildQueryView(View):
    """Build Query View"""

    build_query_url = "core_explore_example_build_query"
    get_query_url = "core_explore_example_get_query"
    save_query_url = "core_explore_example_save_query"
    results_url = "core_explore_example_results"
    select_fields_url = "core_explore_example_select_fields"
    object_name = "template"
    data_sources_selector_template = (
        "core_explore_common_app/user/selector/data_sources_selector" ".html"
    )
    query_builder_interface = (
        "core_explore_example_app/user/query_builder/initial_form.html"
    )

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_EXAMPLE_CONTENT_TYPE,
            permission=rights.EXPLORE_EXAMPLE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, template_id, query_id=None):
        """Page that allows to build and submit queries

        Args:
            request:
            template_id:
            query_id:

        Returns:

        """
        try:
            template = template_api.get_by_id(template_id, request=request)
            if template is None:
                return render(
                    request,
                    "core_explore_example_app/user/errors.html",
                    assets={},
                    context={
                        "errors": "The selected {0} does not exist".format(
                            self.object_name
                        )
                    },
                )

            # Init variables
            saved_query_form = ""

            try:
                explore_data_structure = (
                    explore_data_structure_api.get_by_user_id_and_template_id(
                        str(request.user.id), template_id
                    )
                )
                # If custom fields form present, set it
                custom_form = explore_data_structure.selected_fields_html_tree
            except exceptions.DoesNotExist:
                custom_form = None

            # If new form
            if query_id is None:
                # empty session variables
                request.session["mapCriteriaExplore"] = dict()
                request.session["savedQueryFormExplore"] = ""
                # create new query object
                query = self._create_new_query(request, template)
            else:
                # if not a new form and a query form is present in session
                if "savedQueryFormExplore" in request.session:
                    saved_query_form = request.session["savedQueryFormExplore"]
                query = query_api.get_by_id(query_id, request.user)

            # Get saved queries of a user
            if "_auth_user_id" in request.session:
                user_id = request.session["_auth_user_id"]
                user_queries = saved_query_api.get_all_by_user_and_template(
                    user_id=user_id, template_id=template_id
                )
            else:
                user_queries = []

            assets = {"js": self._get_js(), "css": self._get_css()}

            context = {
                "queries": user_queries,
                "template_id": template_id,
                "description": self.get_description(),
                "title": self.get_title(),
                "data_sorting_fields": build_sorting_context_array(query),
                "default_data_sorting_fields": ",".join(DATA_SORTING_FIELDS),
                "custom_form": custom_form,
                "query_form": saved_query_form,
                "query_id": str(query.id),
                "build_query_url": self.build_query_url,
                "results_url": self.results_url,
                "get_query_url": self.get_query_url,
                "save_query_url": self.save_query_url,
                "select_fields_url": self.select_fields_url,
                "data_sources_selector_template": self.data_sources_selector_template,
                "query_builder_interface": self.query_builder_interface,
            }

            modals = [
                "core_explore_example_app/user/modals/custom_tree.html",
                "core_explore_example_app/user/modals/sub_elements_query_builder.html",
                "core_main_app/common/modals/error_page_modal.html",
                "core_explore_example_app/user/modals/delete_all_queries.html",
                "core_explore_example_app/user/modals/delete_query.html",
            ]

            return render(
                request,
                "core_explore_example_app/user/build_query.html",
                assets=assets,
                context=context,
                modals=modals,
            )
        except Exception as exception:
            return render(
                request,
                "core_explore_example_app/user/errors.html",
                assets={},
                context={"errors": str(exception)},
            )

    @staticmethod
    def _create_new_query(request, template):
        """Create a new query
        Args:
            request:
            template:

        """
        # from the template, we get the version manager
        template_version_manager = template.version_manager
        # from the version manager, we get all the version
        template_ids = template_api.get_all_accessible_by_id_list(
            template_version_manager.versions, request=request
        )
        # create query
        query = query_api.create_default_query(request, template_ids)
        return query

    @staticmethod
    def _get_js():
        return [
            {
                "path": "core_explore_example_app/user/js/build_query.js",
                "is_raw": False,
            },
            {
                "path": "core_explore_example_app/user/js/build_query.raw.js",
                "is_raw": True,
            },
            {"path": "core_parser_app/js/autosave.raw.js", "is_raw": True},
            {"path": "core_parser_app/js/choice.js", "is_raw": False},
            {
                "path": "core_main_app/common/js/modals/error_page_modal.js",
                "is_raw": True,
            },
        ]

    @staticmethod
    def _get_css():
        return [
            "core_explore_common_app/user/css/results.css",
            "core_explore_example_app/user/css/query_builder.css",
            "core_explore_example_app/user/css/xsd_form.css",
        ]

    @staticmethod
    def get_description():
        """get_description

        Returns
        """
        # FIXME should be in template
        return (
            "Click on a field of the Query Builder to add an element to your query. "
            "The elements selected in the previous step will appear and you will be "
            "able to insert them in the query builder. Click on plus/minus icons to "
            "add/remove criteria. You can save queries to build more complex queries "
            "and you will retrieve them on your next connection. When your query is "
            "done, please click on Submit Query to get XML documents that match the "
            "criteria."
        )

    @staticmethod
    def get_title():
        """get_description

        Returns
        """
        return "Query Builder"


class ResultQueryView(ResultsView):
    """Result Query View"""

    back_to_query_redirect = "core_explore_example_build_query"
    get_query_url = "core_explore_example_get_query"

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_EXAMPLE_CONTENT_TYPE,
            permission=rights.EXPLORE_EXAMPLE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, template_id, query_id):
        """Query results view

        Args:
            request:
            template_id:
            query_id:

        Returns:

        """

        # get query
        query = query_api.get_by_id(query_id, request.user)

        context = {
            "template_id": template_id,
            "query_id": query_id,
            "exporter_app": False,
            "back_to_query_redirect": self.back_to_query_redirect,
            "get_query_url": self.get_query_url,
            "default_date_toggle_value": DEFAULT_DATE_TOGGLE_VALUE,
            "data_sorting_fields": super().build_sorting_context_array(query),
            "default_data_sorting_fields": ",".join(DATA_SORTING_FIELDS),
            "back_to_builder": True,
        }

        if "core_exporters_app" in INSTALLED_APPS:
            query = query_api.get_by_id(query_id, request.user)

            context["exporter_app"] = True
            context["templates_list"] = json.dumps(
                [str(template.id) for template in query.templates.all()]
            )

        return render(
            request,
            "core_explore_example_app/user/results.html",
            assets=self.assets,
            modals=self.modals,
            context=context,
        )

    def _load_assets(self):
        assets = super()._load_assets()
        extra_assets = {
            "js": [
                {
                    "path": "core_explore_example_app/user/js/refresh_sorting.raw.js",
                    "is_raw": True,
                },
                {
                    "path": "core_explore_example_app/user/js/refresh_sorting.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_example_app/user/js/persistent_query.raw.js",
                    "is_raw": True,
                },
                {"path": "core_main_app/user/js/data/detail.js", "is_raw": False},
            ],
            "css": [],
        }

        assets["js"].extend(extra_assets["js"])
        assets["css"].extend(extra_assets["css"])

        return assets

    def _load_modals(self):
        """Return modals structure

        Returns:

        """
        return super()._load_modals()


class ResultQueryExampleRedirectView(ResultQueryRedirectView):
    """Result Query Example Redirect View"""

    model_name = PersistentQueryExample.__name__
    object_name = "persistent_query_example"
    redirect_url = "core_explore_example_results"

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_EXAMPLE_CONTENT_TYPE,
            permission=rights.EXPLORE_EXAMPLE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @staticmethod
    def _get_persistent_query_by_id(persistent_query_id, user):
        return persistent_query_example_api.get_by_id(persistent_query_id, user)

    @staticmethod
    def _get_persistent_query_by_name(persistent_query_name, user):
        return persistent_query_example_api.get_by_name(persistent_query_name, user)

    @staticmethod
    def get_url_path():
        return reverse(
            ResultQueryExampleRedirectView.redirect_url,
            kwargs={"template_id": "template_id", "query_id": "query_id"},
        ).split("results")[0]

    @staticmethod
    def _get_reversed_url(query):
        return reverse(
            ResultQueryExampleRedirectView.redirect_url,
            kwargs={"template_id": query.templates.all()[0].id, "query_id": query.id},
        )

    @staticmethod
    def _get_reversed_url_if_failed():
        return reverse("core_explore_example_index")


# FIXME duplicate code in core_explore_common_app
def build_sorting_context_array(query):
    """Get the query data-sources dans build the context sorting array for the JS

    Returns:

    """
    context_array = []
    for data_source in query.data_sources:
        context_array.append(data_source["order_by_field"])

    return ";".join(context_array)
