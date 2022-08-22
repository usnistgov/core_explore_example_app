""" Unit Test Persistent Query Example
"""

from django.contrib.auth.models import AnonymousUser


from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_explore_common_app.settings import CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT
import core_explore_example_app.components.persistent_query_example.api as persistent_query_example_api
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)
from tests.components.persistent_query_example.fixtures.fixtures import (
    PersistentQueryExampleFixtures,
)

fixture_persistent_query_example = PersistentQueryExampleFixtures()


class TestPersistentQueryExampleGetById(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Get By Id"""

    fixture = fixture_persistent_query_example

    def test_get_by_id_as_superuser_returns_persistent_query_example(self):
        """test_get_by_id_as_superuser_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_id = self.fixture.persistent_query_example_1.id
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_example = persistent_query_example_api.get_by_id(
            persistent_query_example_id, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_example, PersistentQueryExample))

    def test_get_by_id_as_owner_returns_persistent_query_example(self):
        """test_get_by_id_as_owner_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_id = self.fixture.persistent_query_example_1.id
        mock_user = create_mock_user("1")

        # Act
        persistent_query_example = persistent_query_example_api.get_by_id(
            persistent_query_example_id, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_example, PersistentQueryExample))

    def test_get_by_id_as_user_not_owner_returns_persistent_query_example(self):
        """test_get_by_id_as_user_not_owner_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_id = self.fixture.persistent_query_example_1.id
        mock_user = create_mock_user("0")

        # Act # Assert
        self.assertTrue(
            isinstance(
                persistent_query_example_api.get_by_id(
                    persistent_query_example_id, mock_user
                ),
                PersistentQueryExample,
            )
        )

    def test_get_by_id_as_anonymous_user(self):
        """test_get_by_id_as_anonymous_user"""

        # Arrange
        persistent_query_example_id = self.fixture.persistent_query_example_1.id

        # Act # Assert
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            self.assertTrue(
                isinstance(
                    persistent_query_example_api.get_by_id(
                        persistent_query_example_id, AnonymousUser()
                    ),
                    PersistentQueryExample,
                )
            )

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_example_api.get_by_id(
                    persistent_query_example_id, AnonymousUser()
                )


class TestPersistentQueryExampleGetByName(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Get By Name"""

    fixture = fixture_persistent_query_example

    def test_get_by_name_as_superuser_returns_persistent_query_example(self):
        """test_get_by_name_as_superuser_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_name = self.fixture.persistent_query_example_1.name
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_example = persistent_query_example_api.get_by_name(
            persistent_query_example_name, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_example, PersistentQueryExample))

    def test_get_by_id_as_owner_returns_persistent_query_example(self):
        """test_get_by_id_as_owner_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_name = self.fixture.persistent_query_example_1.name
        mock_user = create_mock_user("1")

        # Act
        persistent_query_example = persistent_query_example_api.get_by_name(
            persistent_query_example_name, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_example, PersistentQueryExample))

    def test_get_by_id_as_user_not_owner_returns_persistent_query_example(self):
        """test_get_by_id_as_user_not_owner_returns_persistent_query_example"""

        # Arrange
        persistent_query_example_name = self.fixture.persistent_query_example_1.name
        mock_user = create_mock_user("0")

        # Act # Assert
        self.assertTrue(
            isinstance(
                persistent_query_example_api.get_by_name(
                    persistent_query_example_name, mock_user
                ),
                PersistentQueryExample,
            )
        )

    def test_get_by_id_as_anonymous_user(self):
        """test_get_by_id_as_anonymous_user"""

        # Arrange
        persistent_query_example_name = self.fixture.persistent_query_example_1.name

        # Act # Assert
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            self.assertTrue(
                isinstance(
                    persistent_query_example_api.get_by_name(
                        persistent_query_example_name, AnonymousUser()
                    ),
                    PersistentQueryExample,
                )
            )

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_example_api.get_by_name(
                    persistent_query_example_name, AnonymousUser()
                )


class TestPersistentQueryExampleDelete(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Delete"""

    fixture = fixture_persistent_query_example

    def test_delete_others_persistent_query_example_as_superuser_deletes_persistent_query_example(
        self,
    ):
        """test_delete_others_persistent_query_example_as_superuser_deletes_persistent_query_example"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_example_api.delete(persistent_query_example, mock_user)

    def test_delete_own_persistent_query_example_deletes_persistent_query_example(self):
        """test_delete_own_persistent_query_example_deletes_persistent_query_example"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        mock_user = create_mock_user("1")

        # Act
        persistent_query_example_api.delete(persistent_query_example, mock_user)

    def test_delete_others_persistent_query_example_raises_error(self):
        """test_delete_others_persistent_query_example_raises_error"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.delete(persistent_query_example, mock_user)

    def test_delete_others_persistent_query_example_as_anonymous_raises_error(
        self,
    ):
        """test_delete_others_persistent_query_example_as_anonymous_raises_error"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.delete(
                persistent_query_example, AnonymousUser()
            )


class TestPersistentQueryExampleUpdate(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Update"""

    fixture = fixture_persistent_query_example

    def test_update_others_persistent_query_example_as_superuser_updates_data_structure(
        self,
    ):
        """test_update_others_persistent_query_example_as_superuser_updates_data_structure"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        persistent_query_example.name = "new_name_persistent_query_example_1"
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)
        # Act
        result = persistent_query_example_api.upsert(
            persistent_query_example, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryExample))
        self.assertTrue(result.name, "new_name_persistent_query_example_1")

    def test_update_own_persistent_query_example_updates_persistent_query_example(self):
        """test_update_own_persistent_query_example_updates_persistent_query_example"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        mock_user = create_mock_user("1")
        persistent_query_example.name = "new_name_persistent_query_example_1"
        # Act
        result = persistent_query_example_api.upsert(
            persistent_query_example, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryExample))
        self.assertTrue(result.name, "new_name_persistent_query_example_1")

    def test_update_others_persistent_query_example_raises_error(self):
        """test_update_others_persistent_query_example_raises_error"""

        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1
        persistent_query_example.name = "new_name_persistent_query_example_1"
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.upsert(persistent_query_example, mock_user)

    def test_update_others_persistent_query_example_as_anonymous_raises_error(
        self,
    ):
        """test_update_others_persistent_query_example_as_anonymous_raises_error"""
        # Arrange
        persistent_query_example = self.fixture.persistent_query_example_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.upsert(
                persistent_query_example, AnonymousUser()
            )


class TestPersistentQueryExampleCreate(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Create"""

    fixture = fixture_persistent_query_example

    def test_create_others_persistent_query_example_as_superuser_creates_persistent_query_example(
        self,
    ):
        """test_create_others_persistent_query_example_as_superuser_creates_persistent_query_example"""
        # Arrange
        persistent_query_example = PersistentQueryExample(
            name="new_persistent_query_example", user_id="0"
        )
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)
        # Act
        result = persistent_query_example_api.upsert(
            persistent_query_example, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryExample))
        self.assertTrue(result.name, "new_persistent_query_example")

    def test_create_persistent_query_example_as_user_creates_persistent_query_example(
        self,
    ):
        """test_create_persistent_query_example_as_user_creates_persistent_query_example"""

        # Arrange
        persistent_query_example = PersistentQueryExample(
            name="new_persistent_query_example", user_id="1"
        )
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_example_api.upsert(
            persistent_query_example, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryExample))
        self.assertTrue(result.name, "new_persistent_query_example")

    def test_create_persistent_query_example_as_anonymous_user(self):
        """test_create_persistent_query_example_as_anonymous_user"""

        # Arrange
        persistent_query_example = PersistentQueryExample(
            name="new_persistent_query_example", user_id="None"
        )

        # Act
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            result = persistent_query_example_api.upsert(
                persistent_query_example, AnonymousUser()
            )
            # Assert
            self.assertTrue(isinstance(result, PersistentQueryExample))
            self.assertTrue(result.name, "new_persistent_query_example")

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_example_api.upsert(
                    persistent_query_example, AnonymousUser()
                )


class TestPersistentQueryExampleGetAll(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Get All"""

    fixture = fixture_persistent_query_example

    def test_get_all_as_superuser_returns_all_persistent_query_example(self):
        """test_get_all_as_superuser_returns_all_persistent_query_example"""

        # Arrange
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_example_api.get_all(mock_user)

        # Assert
        self.assertTrue(len(result), 3)

    def test_get_all_as_user_raises_error(self):
        """test_get_all_as_user_raises_error"""

        # Arrange
        mock_user = create_mock_user("1")

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.get_all(mock_user)

    def test_get_all_as_anonymous_user_raises_error(self):
        """test_get_all_as_anonymous_user_raises_error"""

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_example_api.get_all(AnonymousUser())


class TestPersistentQueryExampleGetAllByUser(MongoIntegrationBaseTestCase):
    """Test Persistent Query Example Get All By User"""

    fixture = fixture_persistent_query_example

    def test_get_all_by_user_as_superuser_returns_all_user_persistent_query_example(
        self,
    ):
        """test_get_all_by_user_as_superuser_returns_all_user_persistent_query_example"""

        # Arrange
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_example_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)

    def test_get_all_by_user_returns_all_user_persistent_query_example(self):
        """test_get_all_by_user_returns_all_user_persistent_query_example"""

        # Arrange
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_example_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)
