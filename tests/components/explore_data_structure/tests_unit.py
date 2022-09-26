""" Unit Test Explore Data Structure
"""
from unittest.case import TestCase

from unittest.mock import patch

from core_main_app.components.template.models import Template
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_explore_example_app.components.explore_data_structure import (
    api as explore_data_structure_api,
)
from core_explore_example_app.components.explore_data_structure.models import (
    ExploreDataStructure,
)


class TestExploreDataStructureInsert(TestCase):
    """Test Explore Data Structure Insert"""

    @patch.object(ExploreDataStructure, "get_by_user_id_and_template_id")
    @patch.object(ExploreDataStructure, "save")
    def test_explore_data_structure_upsert_single_structure(
        self, mock_save, mock_list
    ):
        """test_explore_data_structure_upsert_single_structure"""

        data = create_explore_data_structure("1", "name_title_1")
        mock_save.return_value = data
        mock_list.return_value = None
        explore_data_structure_api.upsert(data)


class TestExploreDataStructureGetByUserIdAndTemplateId(TestCase):
    """Test Explore Data Structure Get By User Id And TemplateId"""

    @patch.object(ExploreDataStructure, "get_by_user_id_and_template_id")
    def test_explore_data_structure_get_by_user_and_template_returns_explore_data_structure(
        self, mock_list
    ):
        """test_explore_data_structure_get_by_user_and_template_returns_explore_data_structure"""

        # Arrange
        mock_data = create_explore_data_structure(
            user="1", name="name_title_1"
        )
        mock_list.return_value = mock_data
        # Act
        result = explore_data_structure_api.get_by_user_id_and_template_id(
            "1", "1"
        )
        # Assert
        self.assertTrue(isinstance(result, ExploreDataStructure))


def _get_template():
    """Returns a template

    Returns:

    """
    template = Template()
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    return template


def _get_data_structure_element(user, data_structure):
    """Return a data structure element

    Args:
        user:
        data_structure:

    Returns:

    """
    data_structure_element = DataStructureElement(
        user=user,
        tag="tag",
        value="value",
        options={},
        data_structure=data_structure,
    )
    data_structure_element.save()
    return data_structure_element


def create_explore_data_structure(user, name):
    """Creates Explore Data Structure

    Args:
        user:
        name:

    Returns:

    """
    template = _get_template()
    explore_data_structure = ExploreDataStructure(
        user=user,
        template=template,
        name=name,
        data_structure_element_root=None,
    )
    return explore_data_structure
