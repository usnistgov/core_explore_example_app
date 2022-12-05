""" Test user AJAX views
"""
import json
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from django.test import RequestFactory
from rest_framework import status

from core_explore_example_app.views.user.ajax import save_fields, GetQueryView
from core_main_app.commons.exceptions import ModelError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.mocks import MockQueryObject


class TestSaveFields(TestCase):
    """TestSaveFields"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        # bypass permission checks to access view
        self.user1.has_perm = MagicMock()
        self.user1.has_perm.return_value = True

    @mock.patch(
        "core_explore_example_app.components.explore_data_structure.api.get_by_user_id_and_template_id"
    )
    @mock.patch(
        "core_explore_example_app.components.explore_data_structure.api.upsert"
    )
    def test_view_returns_response(
        self, mock_upsert, mock_get_by_user_id_and_template_id
    ):
        """test_view_returns_response

        Returns:

        """
        # Init mocks
        mock_get_by_user_id_and_template_id.return_value = MagicMock()
        mock_upsert.return_value = None
        # Create data payload
        data = {
            "formContent": "test",
            "templateID": "1",
        }

        # Create request
        request = self.factory.post(
            "core_explore_example_save_fields", data=data
        )
        # Set user
        request.user = self.user1

        response = save_fields(request)
        self.assertEqual(response.status_code, 200)

    @mock.patch(
        "core_explore_example_app.components.explore_data_structure.api.get_by_user_id_and_template_id"
    )
    @mock.patch(
        "core_explore_example_app.components.explore_data_structure.api.upsert"
    )
    def test_view_with_bad_input_returns_500_response(
        self, mock_upsert, mock_get_by_user_id_and_template_id
    ):
        """test_view_with_bad_input_returns_500_response

        Returns:

        """
        # Init mocks
        mock_get_by_user_id_and_template_id.return_value = MagicMock()
        mock_upsert.return_value = None
        # Create data payload
        data = {
            "formContent": "te$t",
            "templateID": "1",
        }

        # Create request
        request = self.factory.post(
            "core_explore_example_save_fields", data=data
        )
        # Set user
        request.user = self.user1

        response = save_fields(request)
        self.assertEqual(response.status_code, 400)


class TestGetQueryViewsPost(TestCase):
    """Test GetQueryView post method"""

    def setUp(self):
        """setUp"""
        self.factory = RequestFactory()
        self.view_name = "core_explore_example_get_query"
        self.user1 = create_mock_user(user_id="1")
        # bypass permission checks to access view
        self.user1.has_perm = MagicMock()
        self.user1.has_perm.return_value = True

    def test_request_without_template_id_fails(self):
        """test_request_without_template_id_fails"""
        data = {
            "queryID": "mock_query_id",
            "orderByField": "mock_field_1;mock_field_2",
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_request_without_query_id_fails(self):
        """test_request_without_query_id_fails"""
        data = {
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_request_without_order_by_field_fails(self):
        """test_request_without_order_by_field_fails"""
        data = {"queryID": "mock_query_id", "templateID": "mock_template_id"}

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_query_not_existing_fails(self, mock_query_get_by_id):
        """test_query_not_existing_fails"""
        mock_query_get_by_id.side_effect = ModelError("mock_model_error")
        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_example_app.utils.mongo_query.check_query_form")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_no_data_source_selected_fails(
        self, mock_query_get_by_id, mock_check_query_form
    ):
        """test_no_data_source_selected_fails"""
        mock_query_object = MockQueryObject()
        mock_query_object.data_sources = []

        mock_query_get_by_id.return_value = mock_query_object
        mock_check_query_form.return_value = []

        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_example_app.views.user.ajax.check_query_form")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_errors_in_query_form_fails(
        self, mock_query_get_by_id, mock_check_query_form
    ):
        """test_errors_in_query_form_fails"""
        mock_query_object = MockQueryObject()
        mock_query_object.data_sources = ["mock_data_source_1"]

        mock_query_get_by_id.return_value = mock_query_object
        mock_check_query_form.return_value = ["mock_check_query_form_error"]

        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
            "formValues": json.dumps({"form_value": "mock_form_value"}),
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "core_explore_example_app.views.user.ajax.GetQueryView.fields_to_query_func"
    )
    @patch("core_explore_example_app.views.user.ajax.check_query_form")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_errors_in_query_content_creation_fails(
        self,
        mock_query_get_by_id,
        mock_check_query_form,
        mock_fields_to_query_func,
    ):
        """test_errors_in_query_content_creation_fails"""
        mock_query_object = MockQueryObject()
        mock_query_object.data_sources = [{}]

        mock_query_get_by_id.return_value = mock_query_object
        mock_check_query_form.return_value = []
        mock_fields_to_query_func.side_effect = Exception(
            "mock_fields_to_query_func_exception"
        )

        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
            "formValues": json.dumps({"form_value": "mock_form_value"}),
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_common_app.components.query.api.upsert")
    @patch(
        "core_explore_example_app.views.user.ajax.GetQueryView.fields_to_query_func"
    )
    @patch("core_explore_example_app.views.user.ajax.check_query_form")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_errors_in_query_upsert_fails(
        self,
        mock_query_get_by_id,
        mock_check_query_form,
        mock_fields_to_query_func,
        mock_query_upsert,
    ):
        """test_errors_in_query_upsert_fails"""
        mock_query_object = MockQueryObject()
        mock_query_object.data_sources = [{}]

        mock_query_get_by_id.return_value = mock_query_object
        mock_check_query_form.return_value = []
        mock_fields_to_query_func.return_value = {"mock_field": "mock_value"}
        mock_query_upsert.side_effect = Exception(
            "mock_query_upsert_exception"
        )

        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
            "formValues": json.dumps({"form_value": "mock_form_value"}),
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_common_app.components.query.api.upsert")
    @patch(
        "core_explore_example_app.views.user.ajax.GetQueryView.fields_to_query_func"
    )
    @patch("core_explore_example_app.views.user.ajax.check_query_form")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_success_returns_200_status_code(
        self,
        mock_query_get_by_id,
        mock_check_query_form,
        mock_fields_to_query_func,
        mock_query_upsert,
    ):
        """test_success_returns_200_status_code"""
        mock_query_object = MockQueryObject()
        mock_query_object.data_sources = [{}]

        mock_query_get_by_id.return_value = mock_query_object
        mock_check_query_form.return_value = []
        mock_fields_to_query_func.return_value = {"mock_field": "mock_value"}
        mock_query_upsert.return_value = None

        data = {
            "queryID": "mock_query_id",
            "templateID": "mock_template_id",
            "orderByField": "mock_field_1;mock_field_2",
            "formValues": json.dumps({"form_value": "mock_form_value"}),
        }

        request = self.factory.post(self.view_name, data=data)
        request.user = self.user1

        self.assertEqual(
            GetQueryView().post(request).status_code,
            status.HTTP_200_OK,
        )
