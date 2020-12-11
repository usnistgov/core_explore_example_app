""" Integration Test for Persistent Query Example Rest API
"""

from tests.components.persistent_query_example.fixtures.fixtures import (
    PersistentQueryExampleFixtures,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_explore_example_app.rest.persistent_query_example import (
    views as persistent_query_example_views,
)

from rest_framework import status
from core_explore_common_app.settings import CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from django.contrib.auth.models import AnonymousUser


fixture_data_structure = PersistentQueryExampleFixtures()


class TestPersistentQueryExampleListAdmin(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def setUp(self):
        super(TestPersistentQueryExampleListAdmin, self).setUp()

        self.user = create_mock_user("1", is_staff=True, is_superuser=True)

        self.data = {
            "user_id": "1",
            "name": "persistent_query_name",
        }

    def test_get_returns_all_user_persistent_query_example(self):
        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            self.user,
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_post_returns_http_201(self):
        # Arrange

        # Act
        response = RequestMock.do_request_post(
            persistent_query_example_views.AdminPersistentQueryExampleList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryExampleList(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def setUp(self):
        super(TestPersistentQueryExampleList, self).setUp()

        self.user = create_mock_user("1")

        self.data = {
            "name": "persistent_query_name",
        }

    def test_get_returns_all_persistent_query_example(self):
        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            self.user,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_returns_http_201(self):

        # Act
        response = RequestMock.do_request_post(
            persistent_query_example_views.PersistentQueryExampleList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryExampleDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def setUp(self):
        super(TestPersistentQueryExampleDetail, self).setUp()

    def test_get_returns_http_200(self):
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

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            AnonymousUser(),
            param={"pk": str(self.fixture.persistent_query_example_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_returns_http_204(self):
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
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_other_user_persistent_query_example_returns_http_403(self):
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
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            persistent_query_example_views.PersistentQueryExampleDetail.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPersistentQueryExampleByName(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def setUp(self):
        super(TestPersistentQueryExampleByName, self).setUp()

    def test_get_returns_http_200(self):
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

    def test_get_other_user_persistent_query_example_by_name_as_anonymous_user(self):

        # Act
        response = RequestMock.do_request_get(
            persistent_query_example_views.PersistentQueryExampleByName.as_view(),
            AnonymousUser(),
            param={"name": str(self.fixture.persistent_query_example_1.name)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_name_returns_http_404(self):
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
