""" Authentication tests for Saved Query REST API
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_explore_example_app.components.saved_query.api as saved_query_api
from core_explore_example_app.components.saved_query.models import SavedQuery
from core_explore_example_app.rest.saved_query.serializers import (
    SavedQuerySerializer,
)
from core_explore_example_app.rest.saved_query.views import (
    SavedQueryList,
    SavedQueryDetail,
)


class TestSavedQueryListGetPermissions(SimpleTestCase):
    """Test Saved Query List Get Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(SavedQueryList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(saved_query_api, "get_all")
    def test_authenticated_returns_http_200(self, mock_saved_query_get_all):
        """test_authenticated_returns_http_200"""

        mock_saved_query_get_all.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            SavedQueryList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(saved_query_api, "get_all")
    def test_staff_returns_http_200(self, mock_saved_query_get_all):
        """test_staff_returns_http_200"""

        mock_saved_query_get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            SavedQueryList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSavedQueryDetailGetPermissions(SimpleTestCase):
    """Test Saved Query Detail Get Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            SavedQueryDetail.as_view(), None, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(saved_query_api, "get_by_id")
    @patch.object(SavedQuerySerializer, "data")
    def test_authenticated_returns_http_200(
        self, mock_saved_query_serializer, mock_saved_query_get_by_id
    ):
        """test_authenticated_returns_http_200"""

        mock_saved_query_get_by_id.return_value = None
        mock_saved_query_serializer.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            SavedQueryDetail.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(saved_query_api, "get_by_id")
    @patch.object(SavedQuerySerializer, "data")
    def test_staff_returns_http_200(
        self, mock_saved_query_serializer, mock_saved_query_get_by_id
    ):
        """test_staff_returns_http_200"""

        mock_saved_query_get_by_id.return_value = None
        mock_saved_query_serializer.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            SavedQueryDetail.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSavedQueryDetailDeletePermissions(SimpleTestCase):
    """Test Saved Query Detail Delete Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_delete(
            SavedQueryDetail.as_view(), None, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(saved_query_api, "get_by_id")
    def test_not_owner_returns_http_403(self, mock_saved_query_get_by_id):
        """test_not_owner_returns_http_403"""

        mock_saved_query_get_by_id.return_value = SavedQuery(user_id="1")
        mock_user = create_mock_user("2")

        response = RequestMock.do_request_delete(
            SavedQueryDetail.as_view(), mock_user, param={"pk": "0"}, data=None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(saved_query_api, "get_by_id")
    @patch.object(saved_query_api, "delete")
    def test_owner_returns_http_204(
        self, mock_saved_query_delete, mock_saved_query_get_by_id
    ):
        """test_owner_returns_http_204"""

        mock_saved_query_get_by_id.return_value = SavedQuery(user_id="1")
        mock_saved_query_delete.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            SavedQueryDetail.as_view(), mock_user, param={"pk": "0"}, data=None
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(saved_query_api, "get_by_id")
    @patch.object(saved_query_api, "delete")
    def test_staff_returns_http_204(
        self, mock_saved_query_delete, mock_saved_query_get_by_id
    ):
        """test_staff_returns_http_204"""

        mock_saved_query_get_by_id.return_value = SavedQuery(user_id="1")
        mock_saved_query_delete.return_value = None
        mock_user = create_mock_user("5", is_staff=True)

        response = RequestMock.do_request_delete(
            SavedQueryDetail.as_view(), mock_user, param={"pk": "0"}, data=None
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
