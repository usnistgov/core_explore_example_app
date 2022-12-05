""" Unit tests for XML utilities.
"""
from unittest import TestCase

from core_explore_example_app.utils.xml import validate_element_value


class TestValidateElementValue(TestCase):
    """Test validate_element_value function"""

    def test_float_type_fails_if_not_float(self):
        """test_float_type_fails_if_not_float"""
        self.assertIsNotNone(
            validate_element_value(
                "mock_element", "xs:float", "mock_wrong_value", "xs"
            )
        )

    def test_float_type_works_if_float(self):
        """test_float_type_works_if_float"""
        self.assertIsNone(
            validate_element_value("mock_element", "xs:float", "7.0", "xs")
        )

    def test_int_type_fails_if_not_int(self):
        """test_int_type_fails_if_not_int"""
        self.assertIsNotNone(
            validate_element_value(
                "mock_element", "xs:int", "mock_wrong_value", "xs"
            )
        )

    def test_int_type_works_if_int(self):
        """test_int_type_works_if_int"""
        self.assertIsNone(
            validate_element_value("mock_element", "xs:int", "5", "xs")
        )

    def test_str_type_fails_if_not_valid(self):
        """test_str_type_fails_if_not_valid"""
        self.assertIsNotNone(
            validate_element_value(
                "mock_element", "xs:string", "$mock_wrong_value", "xs"
            )
        )

    def test_str_type_works_if_valid(self):
        """test_str_type_works_if_valid"""
        self.assertIsNone(
            validate_element_value(
                "mock_element", "xs:string", "mock_string", "xs"
            )
        )
