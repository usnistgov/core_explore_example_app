"""Integration tests for Saved Query rest api
"""

from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_explore_example_app.rest.saved_query.views as saved_query_views
from tests.rest.saved_query.fixtures.fixtures import SavedQueryFixtures

fixture_data = SavedQueryFixtures()


class TestGetSavedQueryList(IntegrationBaseTestCase):
    """Test Get Saved Query List"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_get_all_returns_status_200_with_no_permission_needed(self):
        """test_get_all_returns_status_200_with_no_permission_needed"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            saved_query_views.SavedQueryList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetSavedQueryDetail(IntegrationBaseTestCase):
    """Test Get Saved Query Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_get_returns_object_when_found(self):
        """test_get_returns_object_when_found"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_get(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_raise_404_when_not_found(self):
        """test_get_raise_404_when_not_found"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_get(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raise_500_sever_error_when_general_error_occurred(self):
        """test_get_raise_500_sever_error_when_general_error_occurred"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_get(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestDeleteSavedQueryDetail(IntegrationBaseTestCase):
    """Test Delete Saved Query Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super(TestDeleteSavedQueryDetail, self).setUp()
        self.data = None

    def test_delete_returns_403_status_when_user_is_unhautorized(self):
        """test_delete_returns_403_status_when_user_is_unhautorized"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_delete(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_returns_204_status_when_found(self):
        """test_delete_returns_204_status_when_found"""

        # Arrange
        user = create_mock_user("1")
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_delete(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_raise_404_when_not_found(self):
        """test_delete_raise_404_when_not_found"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_delete(
            saved_query_views.SavedQueryDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
