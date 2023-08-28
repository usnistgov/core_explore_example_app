""" Test user views
"""

from tests.components.data.fixtures.fixtures import (
    DataFixtures,
)

from core_explore_example_app.views.user.views import IndexView
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestIndexView(IntegrationBaseTestCase):
    """TestIndexView"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fixture = DataFixtures()
        self.fixture.insert_data()
        self.user1 = create_mock_user(user_id="1")

    def test_get_global_active_list_returns_xsd_templates(
        self,
    ):
        """test_get_global_active_list_returns_xsd_templates

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.user1)

        # Act
        index_view = IndexView()
        templates = index_view.get_global_active_list(mock_request)

        # Assert
        self.assertEqual(templates.count(), 1)
        self.assertEqual(templates[0], self.fixture.global_template_vm_xsd)

    def test_get_user_active_list_returns_xsd_templates(
        self,
    ):
        """test_get_user_active_list_returns_xsd_templates

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.user1)

        # Act
        index_view = IndexView()
        templates = index_view.get_user_active_list(mock_request)

        # Assert
        self.assertEqual(templates.count(), 1)
        self.assertEqual(templates[0], self.fixture.user_template_vm_xsd)
