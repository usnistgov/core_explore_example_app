""" Integration Test for Persistent Query Example Rest API
"""

from django.contrib.auth.models import AnonymousUser
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_explore_example_app.rest.persistent_query_example import (
    views as persistent_query_example_views,
)
from tests.components.persistent_query_example.fixtures.fixtures import (
    PersistentQueryExampleFixtures,
)

fixture_data_structure = PersistentQueryExampleFixtures()


class TestPersistentQueryExampleListAdmin(IntegrationBaseTestCase):
    """Test Persistent Query Example List Admin"""

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""

        super().setUp()

        self.user = create_mock_user("1", is_staff=True, is_superuser=True)

        self.data = {
            "user_id": "1",
            "name": "persistent_query_name",
        }

    def test_get_returns_all_user_persistent_query_example(self):
        """test_get_returns_all_user_persistent_query_example"""

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            self.user,
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_post_returns_http_201(self):
        """test_post_returns_http_201"""

        # Arrange

        # Act
        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryExampleList(IntegrationBaseTestCase):
    """Test Persistent Query Example List"""

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""

        super().setUp()

        self.user = create_mock_user("1")

        self.data = {
            "name": "persistent_query_name",
        }

    def test_get_returns_all_persistent_query_example(self):
        """test_get_returns_all_persistent_query_example"""

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            self.user,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_returns_http_201(self):
        """test_post_returns_http_201"""

        # Act
        response = RequestMock.do_request_post(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryExampleDetail(IntegrationBaseTestCase):
    """Test Persistent Query Example Detail"""

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_persistent_query_example(self):
        """test_get_returns_persistent_query_example"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(
            response.data["name"], self.fixture.persistent_query_example_1.name
        )

    def test_get_other_user_persistent_query_example_returns_persistent_query_example(
        self,
    ):
        """test_get_other_user_persistent_query_example_returns_persistent_query_example"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(
            response.data["name"], self.fixture.persistent_query_example_1.name
        )

    def test_get_other_user_persistent_query_example_as_anonymous_user(self):
        """test_get_other_user_persistent_query_example_as_anonymous_user"""

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            AnonymousUser(),
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_returns_http_204(self):
        """test_delete_returns_http_204"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_persistent_query_example_returns_http_403(self):
        """test_delete_other_user_persistent_query_example_returns_http_403"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wrong_id_returns_http_404(self):
        """test_delete_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_other_user_persistent_query_example_returns_http_403(self):
        """test_patch_other_user_persistent_query_example_returns_http_403"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_returns_updated_name(self):
        """test_patch_returns_updated_name"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
            data={"name": "new_name"},
        )

        # Assert
        self.assertEqual(response.data["name"], "new_name")

    def test_patch_wrong_id_returns_http_404(self):
        """test_patch_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPersistentQueryExampleByName(IntegrationBaseTestCase):
    """Test Persistent Query Example By Name"""

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            user,
            param={"name": str(self.fixture.persistent_query_example_1.name)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_name_returns_persistent_query_example(self):
        """test_get_by_name_returns_persistent_query_example"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            user,
            param={"name": str(self.fixture.persistent_query_example_1.name)},
        )

        # Assert
        self.assertEqual(
            response.data["name"], self.fixture.persistent_query_example_1.name
        )

    def test_get_other_user_persistent_query_example_by_name_returns_persistent_query_example(
        self,
    ):
        """test_get_other_user_persistent_query_example_by_name_returns_persistent_query_example"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            user,
            param={"name": str(self.fixture.persistent_query_example_1.name)},
        )

        # Assert
        self.assertEqual(
            response.data["name"], self.fixture.persistent_query_example_1.name
        )

    def test_get_other_user_persistent_query_example_by_name_as_anonymous_user(
        self,
    ):
        """test_get_other_user_persistent_query_example_by_name_as_anonymous_user"""

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            AnonymousUser(),
            param={"name": str(self.fixture.persistent_query_example_1.name)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_name_returns_http_404(self):
        """test_get_wrong_name_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            user,
            param={"name": ""},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
