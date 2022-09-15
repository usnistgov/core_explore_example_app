""" Build Criteria Regression Test
"""
from unittest.case import TestCase

from core_explore_example_app.utils.mongo_query import (
    build_or_criteria,
    build_and_criteria,
    build_wildcard_elem_match_criteria,
)

mock_criteria_1 = {"root.variable": "value"}
mock_criteria_2 = {"root.variable.#text": "value"}
mock_criteria_3 = {"root.variable1": "value"}
mock_criteria_4 = {"root.variable1.#text": "value"}


class TestBuildOrCriteria(TestCase):
    """Test Build Or Criteria"""

    def test_build_or_criteria_regression_with_two_params(self):
        """test_build_or_criteria_regression_with_two_params"""

        # get the result from the old version which allow 2 params
        build_or_criteria_with_two_params_result = (
            self._build_or_criteria_with_two_params(mock_criteria_1, mock_criteria_2)
        )
        # get the result from the new version which allow N params
        build_or_criteria_result = build_or_criteria(mock_criteria_1, mock_criteria_2)

        self.assertDictEqual(
            build_or_criteria_result, build_or_criteria_with_two_params_result
        )

    def test_build_or_criteria_with_one_params(self):
        """test_build_or_criteria_with_one_params"""

        build_or_criteria_result = build_or_criteria(*[mock_criteria_1])

        self.assertDictEqual(build_or_criteria_result, {"$or": [mock_criteria_1]})

    def test_build_or_criteria_with_four_params(self):
        """test_build_or_criteria_with_four_params"""

        build_or_criteria_result = build_or_criteria(
            *[
                mock_criteria_1,
                mock_criteria_2,
                mock_criteria_3,
                mock_criteria_4,
            ]
        )

        self.assertDictEqual(
            build_or_criteria_result,
            {
                "$or": [
                    mock_criteria_1,
                    mock_criteria_2,
                    mock_criteria_3,
                    mock_criteria_4,
                ]
            },
        )

    def _build_or_criteria_with_two_params(self, criteria1, criteria2):
        """Builds a criteria that is the result of criteria1 or criteria2

        Args:
            criteria1:
            criteria2:

        Returns:

        """
        or_criteria = dict()
        or_criteria["$or"] = []
        or_criteria["$or"].append(criteria1)
        or_criteria["$or"].append(criteria2)
        return or_criteria


class TestBuildAndCriteria(TestCase):
    """Test Build And Criteria"""

    def test_build_and_criteria_regression_with_one_params(self):
        """test_build_and_criteria_regression_with_one_params"""

        # get the result from the old version which allow 2 params
        build_and_criteria_with_two_params_result = (
            self._build_and_criteria_with_two_params(mock_criteria_1, mock_criteria_2)
        )
        # get the result from the new version which allow N params
        build_and_criteria_result = build_and_criteria(mock_criteria_1, mock_criteria_2)

        self.assertDictEqual(
            build_and_criteria_result, build_and_criteria_with_two_params_result
        )

    def test_build_and_criteria_with_one_params(self):
        """test_build_and_criteria_with_one_params"""

        build_and_criteria_result = build_and_criteria(*[mock_criteria_1])

        self.assertDictEqual(build_and_criteria_result, {"$and": [mock_criteria_1]})

    def test_build_and_criteria_with_four_params(self):
        """test_build_and_criteria_with_four_params"""

        build_and_criteria_result = build_and_criteria(
            *[
                mock_criteria_1,
                mock_criteria_2,
                mock_criteria_3,
                mock_criteria_4,
            ]
        )

        self.assertDictEqual(
            build_and_criteria_result,
            {
                "$and": [
                    mock_criteria_1,
                    mock_criteria_2,
                    mock_criteria_3,
                    mock_criteria_4,
                ]
            },
        )

    def _build_and_criteria_with_two_params(self, criteria1, criteria2):
        """Builds a criteria that is the result of criteria1 and criteria2

        Args:
            criteria1:
            criteria2:

        Returns:

        """
        and_criteria = dict()
        and_criteria["$and"] = []
        and_criteria["$and"].append(criteria1)
        and_criteria["$and"].append(criteria2)
        return and_criteria


class TestBuildWildcardCriteria(TestCase):
    """Test Build Wildcard Criteria"""

    def test_build_wildcard_criteria_regression_with_one_params(self):
        """test_build_wildcard_criteria_regression_with_one_params"""

        # get the result from the old version which allow 2 params
        build_wildcard_criteria_with_two_params_result = (
            self._build_wildcard_elem_match_criteria(mock_criteria_1, mock_criteria_2)
        )
        # get the result from the new version which allow N params
        build_wildcard_criteria_result = build_wildcard_elem_match_criteria(
            mock_criteria_1, mock_criteria_2
        )

        self.assertDictEqual(
            build_wildcard_criteria_result,
            build_wildcard_criteria_with_two_params_result,
        )

    def test_build_wildcard_criteria_with_one_params(self):
        """test_build_wildcard_criteria_with_one_params"""

        build_wildcard_criteria_result = build_wildcard_elem_match_criteria(
            *[mock_criteria_1]
        )

        self.assertDictEqual(
            build_wildcard_criteria_result,
            {"list_content": {"$elemMatch": {"root.variable": "value"}}},
        )

    def test_build_and_criteria_with_four_params(self):
        """test_build_and_criteria_with_four_params"""

        build_wildcard_criteria_result = build_wildcard_elem_match_criteria(
            *[mock_criteria_1, mock_criteria_2, mock_criteria_3, mock_criteria_4]
        )

        self.assertDictEqual(
            build_wildcard_criteria_result,
            {
                "list_content": {
                    "$elemMatch": {
                        "root.variable": "value",
                        "root.variable.#text": "value",
                        "root.variable1": "value",
                        "root.variable1.#text": "value",
                    }
                }
            },
        )

    def _build_wildcard_elem_match_criteria(self, criteria1, criteria2):
        """Builds a criteria that is the result of criteria1 elemMatch criteria2

        Args:
            criteria1:
            criteria2:

        Returns:

        """
        elem_match_criteria = dict()
        elem_match_criteria["$elemMatch"] = {}
        elem_match_criteria["$elemMatch"].update(criteria1)
        elem_match_criteria["$elemMatch"].update(criteria2)
        return {"list_content": elem_match_criteria}
