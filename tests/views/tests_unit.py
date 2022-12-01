""" Test  views
"""
from unittest import TestCase, mock
from unittest.mock import MagicMock

from django.test import RequestFactory

from core_explore_example_app.views.user.ajax import save_fields
from core_main_app.utils.tests_tools.MockUser import create_mock_user


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
