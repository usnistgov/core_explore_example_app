""" Authentication tests for PersistentQueryExample REST API.
"""
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status

import core_explore_example_app.components.persistent_query_example.api as persistent_query_example_api
from core_explore_example_app.rest.persistent_query_example import (
    views as persistent_query_example_views,
)
from core_explore_example_app.rest.persistent_query_example.serializers import (
    PersistentQueryExampleSerializer,
    PersistentQueryExampleAdminSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from django.contrib.auth.models import AnonymousUser


class TestAdminPersistentQueryExampleListGet(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryExample, "get_all")
    def test_superuser_returns_http_200(self, get_all):
        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryExampleListGet(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryExample, "get_all")
    def test_authenticated_returns_http_200(self, get_all):
        get_all.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(PersistentQueryExample, "get_all")
    def test_superuser_returns_http_200(self, get_all):
        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryExampleListPost(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryExampleSerializer, "is_valid")
    @patch.object(PersistentQueryExampleSerializer, "save")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_authenticated_returns_http_201(
        self,
        persistent_query_example_serializer_data,
        persistent_query_example_serializer_save,
        persistent_query_example_serializer_is_valid,
    ):
        persistent_query_example_serializer_is_valid.return_value = True
        persistent_query_example_serializer_save.return_value = None
        persistent_query_example_serializer_data.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(PersistentQueryExampleAdminSerializer, "is_valid")
    @patch.object(PersistentQueryExampleAdminSerializer, "save")
    @patch.object(PersistentQueryExampleAdminSerializer, "data")
    def test_superuser_returns_http_201(
        self,
        persistent_query_example_serializer_data,
        persistent_query_example_serializer_save,
        persistent_query_example_serializer_is_valid,
    ):
        persistent_query_example_serializer_is_valid.return_value = True
        persistent_query_example_serializer_save.return_value = None
        persistent_query_example_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAdminPersistentQueryExampleListPost(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryExampleAdminSerializer, "is_valid")
    @patch.object(PersistentQueryExampleAdminSerializer, "save")
    @patch.object(PersistentQueryExampleAdminSerializer, "data")
    def test_superuser_returns_http_201(
        self,
        persistent_query_example_serializer_data,
        persistent_query_example_serializer_save,
        persistent_query_example_serializer_is_valid,
    ):
        persistent_query_example_serializer_is_valid.return_value = True
        persistent_query_example_serializer_save.return_value = None
        persistent_query_example_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryExampleDetailGet(SimpleTestCase):
    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_anonymous_returns_http_403(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_id,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_id.return_value = None
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_id,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_id,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryExampleDetailPatch(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(PersistentQueryExampleSerializer, "is_valid")
    @patch.object(PersistentQueryExampleSerializer, "save")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_example_data,
        mock_persistent_query_example_save,
        mock_persistent_query_example_is_valid,
        mock_persistent_query_example_api_get_by_id,
    ):
        mock_persistent_query_example_data.return_value = {}
        mock_persistent_query_example_save.return_value = None
        mock_persistent_query_example_is_valid.return_value = True
        mock_persistent_query_example_api_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(PersistentQueryExampleSerializer, "is_valid")
    @patch.object(PersistentQueryExampleSerializer, "save")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_example_data,
        mock_persistent_query_example_save,
        mock_persistent_query_example_is_valid,
        mock_persistent_query_example_api_get_by_id,
    ):
        mock_persistent_query_example_data.return_value = {}
        mock_persistent_query_example_save.return_value = None
        mock_persistent_query_example_is_valid.return_value = True
        mock_persistent_query_example_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryExampleDetailDelete(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(persistent_query_example_api, "delete")
    def test_authenticated_returns_http_200(
        self, persistent_query_example_api_delete, persistent_query_example_get_by_id
    ):

        persistent_query_example_api_delete.return_value = None
        persistent_query_example_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(persistent_query_example_api, "get_by_id")
    @patch.object(persistent_query_example_api, "delete")
    def test_superuser_returns_http_200(
        self, persistent_query_example_api_delete, persistent_query_example_get_by_id
    ):
        persistent_query_example_api_delete.return_value = None
        persistent_query_example_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPersistentQueryExampleByNameGet(SimpleTestCase):
    @patch.object(persistent_query_example_api, "get_by_name")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_anonymous_returns_http_403(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_name,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_name.return_value = None
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            AnonymousUser(),
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_example_api, "get_by_name")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_name,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_name.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            mock_user,
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_example_api, "get_by_name")
    @patch.object(PersistentQueryExampleSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_example_serializer_data,
        mock_persistent_query_example_api_get_by_name,
    ):
        mock_persistent_query_example_serializer_data.return_value = {}
        mock_persistent_query_example_api_get_by_name.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            mock_user,
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
