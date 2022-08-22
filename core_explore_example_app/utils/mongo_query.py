"""Util to build queries for mongo db
"""
import json
import re
from typing import List, Any

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template import api as template_api
from core_main_app.utils.xml import xpath_to_dot_notation
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from xml_utils.xsd_tree.operations.namespaces import get_namespaces, get_default_prefix
from xml_utils.xsd_types.xsd_types import (
    get_xsd_numbers,
    get_xsd_floating_numbers,
    get_xsd_gregorian_types,
)
from core_explore_example_app.commons.exceptions import MongoQueryException
from core_explore_example_app.components.saved_query import api as saved_query_api
from core_explore_example_app.utils.query_builder import (
    get_element_value,
    get_element_comparison,
)
from core_explore_example_app.utils.xml import validate_element_value


def build_query_criteria(query, is_not=False):
    """Builds a criteria for a query

    Args:
        query:
        is_not:

    Returns:

    """
    if is_not:
        return invert_query(query.copy())
    else:
        return query


def build_int_criteria(path, comparison, value):
    """Builds a criteria for the type integer

    Args:
        path:
        comparison:
        value:

    Returns:

    """
    criteria = dict()

    if comparison == "=":
        criteria[path] = int(value)
    else:
        criteria[path] = json.loads('{{"${0}": {1} }}'.format(comparison, int(value)))

    return criteria


def build_float_criteria(path, comparison, value):
    """Builds a criteria for the type float

    Args:
        path:
        comparison:
        value:

    Returns:

    """
    criteria = dict()

    if comparison == "=":
        criteria[path] = float(value)
    else:
        criteria[path] = json.loads('{{"${0}": {1} }}'.format(comparison, float(value)))

    return criteria


def build_string_criteria(path, comparison, value):
    """Builds a criteria for the type string

    Args:
        path:
        comparison:
        value:

    Returns:

    """
    criteria = dict()

    if comparison == "is":
        criteria[path] = value
    elif comparison == "like":
        criteria[path] = "/" + value + "/"

    return criteria


def build_and_criteria(*criteria_list):
    """Builds a criteria that is the result of and operator for N criteria

    Args:
        criteria_list:

    Returns:

    """
    and_criteria = dict()
    and_criteria["$and"] = []

    for criteria in criteria_list:
        and_criteria["$and"].append(criteria)

    return and_criteria


def build_or_criteria(*criteria_list):
    """Builds a criteria that is the result of or operator for N criteria

    Args:
        criteria_list:

    Returns:

    """
    or_criteria = dict()
    or_criteria["$or"] = []

    for criteria in criteria_list:
        or_criteria["$or"].append(criteria)

    return or_criteria


def build_wildcard_elem_match_criteria(*criteria_list):
    # FIXME: Wildcard method should be move to the example type app
    # FIXME: Mongo_query could be an util class and be inherited as needed
    """Builds a criteria that is the result of N criteria elemMatch

    Args:
        criteria_list:

    Returns:

    """
    elem_match_criteria = dict()
    elem_match_criteria["$elemMatch"] = {}

    for criteria in criteria_list:
        elem_match_criteria["$elemMatch"].update(criteria)

    return {"list_content": elem_match_criteria}


def build_wildcard_criteria(criteria):
    # FIXME: Wildcard method should be move to the example type app
    # FIXME: Mongo_query could be an util class and be inherited as needed
    """Build wildcard criteria, from criteria.

    Args:
        criteria:

    Returns:

    """
    key, value = criteria.popitem()
    criteria_key = {"path": "/.*{}/".format(key)}
    criteria_value = {"value": value}
    return build_wildcard_elem_match_criteria(criteria_key, criteria_value)


def build_criteria(
    element_path,
    comparison,
    value,
    element_type,
    default_prefix,
    is_not=False,
    use_wildcard=False,
):
    """Looks at element type and route to the right function to build the criteria

    Args:
        element_path:
        comparison:
        value:
        element_type:
        default_prefix:
        is_not:
        use_wildcard:

    Returns:

    """
    element_query: List[Any] = []
    attribute_query: List[Any] = []
    # build the query: value can be found at element:value or at element.#text:value
    # second case appends when the element has attributes or namespace information
    if element_type in get_xsd_floating_numbers(default_prefix):
        element_query.append(build_float_criteria(element_path, comparison, value))
        attribute_query.append(
            build_float_criteria("{}.#text".format(element_path), comparison, value)
        )
    elif element_type in get_xsd_numbers(default_prefix):
        element_query.append(build_int_criteria(element_path, comparison, value))
        attribute_query.append(
            build_int_criteria("{}.#text".format(element_path), comparison, value)
        )
    elif element_type in get_xsd_gregorian_types(default_prefix):
        # before creating the int query check if the value type is int
        try:
            int_value = int(value)
            # if the format is number perform a strict match
            attribute_query.append(
                build_int_criteria("{}.#text".format(element_path), "=", int_value)
            )
            element_query.append(build_int_criteria(element_path, "=", int_value))
        except Exception:
            pass

        # string query
        element_query.append(build_string_criteria(element_path, comparison, value))
        attribute_query.append(
            build_string_criteria("{}.#text".format(element_path), comparison, value)
        )

    else:
        element_query.append(build_string_criteria(element_path, comparison, value))
        attribute_query.append(
            build_string_criteria("{}.#text".format(element_path), comparison, value)
        )

    if use_wildcard:
        element_query.append(build_wildcard_criteria(element_query))
        attribute_query.append(build_wildcard_criteria(attribute_query))

    # add a $or operator
    criteria = build_or_criteria(*(element_query + attribute_query))

    if is_not:
        return invert_query(criteria)
    else:
        return criteria


def invert_query(query):
    """Inverts each field of the query to build NOT(query)

    Args:
        query:

    Returns:

    """
    for key, value in list(query.items()):
        if key == "$and" or key == "$or":
            # Invert the query for the case value can be found at element:value or at
            # element.#text:value. Second case happens when the element has attributes
            # or namespace information.
            if (
                len(value) == 2
                and len(list(value[0].keys())) == 1
                and len(list(value[1].keys())) == 1
                and list(value[1].keys())[0]
                == "{}.#text".format(list(value[0].keys())[0])
            ):
                # second query is the same as the first
                if key == "$and":
                    return {"$or": [invert_query(value[0]), invert_query(value[1])]}
                elif key == "$or":
                    return {"$and": [invert_query(value[0]), invert_query(value[1])]}
            for sub_value in value:
                invert_query(sub_value)
        else:
            # lt, lte, =, gte, gt, not, ne
            if isinstance(value, dict):
                if list(value.keys())[0] == "$not" or list(value.keys())[0] == "$ne":
                    query[key] = value[list(value.keys())[0]]
                else:
                    saved_value = value
                    query[key] = dict()
                    query[key]["$not"] = saved_value
            else:
                saved_value = value
                if is_regex(value):
                    query[key] = dict()
                    query[key]["$not"] = saved_value
                else:
                    query[key] = dict()
                    query[key]["$ne"] = saved_value
    return query


def is_regex(expr):
    """Returns true if the expression is a regular expression

    Args:
        expr:

    Returns:

    """
    if isinstance(expr, re.Pattern):
        return True

    try:
        return expr.startswith("/") and expr.endswith("/")
    except:
        return False


def get_dot_notation_to_element(data_structure_element, namespaces):
    """

    Args:
        data_structure_element:
        namespaces:

    Returns:

    """
    # get data structure element's xml xpath
    xml_xpath = data_structure_element.options["xpath"]["xml"]
    # transform xml xpath to dot notation
    dot_notation = xpath_to_dot_notation(xml_xpath, namespaces)

    return dot_notation


def get_parent_name(data_structure_element_id, namespaces, request):
    """

    Args:
        data_structure_element_id:
        namespaces:
        request:

    Returns:

    """
    # get the data structure element
    data_structure_element = data_structure_element_api.get_by_id(
        data_structure_element_id, request
    )
    # convert xml path to mongo dot notation
    data_structure_element_dot_notation = get_dot_notation_to_element(
        data_structure_element, namespaces
    )
    # get parent name
    parent_name = data_structure_element_dot_notation.split(".")[-2]

    return parent_name


def get_parent_path(data_structure_element_id, namespaces, request):
    """

    Args:
        data_structure_element_id:
        namespaces:
        request:

    Returns:

    """
    # get the data structure element
    data_structure_element = data_structure_element_api.get_by_id(
        data_structure_element_id, request
    )
    # convert xml path to mongo dot notation
    data_structure_element_dot_notation = get_dot_notation_to_element(
        data_structure_element, namespaces
    )
    # get path to parent element
    parent_path = ".".join(data_structure_element_dot_notation.split(".")[:-1])

    return parent_path


def check_query_form(form_values, template_id, request=None):
    """Checks that values entered by the user match each element type

    Args:
        form_values:
        template_id:
        request:

    Returns:

    """
    template = template_api.get_by_id(template_id, request=request)
    namespaces = get_namespaces(template.content)
    default_prefix = get_default_prefix(namespaces)

    # check if there are no errors in the query
    errors = []

    if len(form_values) == 0:
        errors.append("The query is empty.")

    for field in form_values:
        element_value = get_element_value(field)
        element_name = field.get("name", "Unnamed field")
        element_type = field.get("type", None)
        # If there is a type to check
        if element_type:
            error = validate_element_value(
                element_name, element_type, element_value, default_prefix
            )
            if error is not None:
                errors.append(error)

    return errors


def fields_to_query(form_values, template_id, use_wildcard=False, request=None):
    """Takes values from the html tree and creates a query from them

    Args:
        form_values:
        template_id:
        use_wildcard:
        request:
    Returns:

    """
    # get template
    template = template_api.get_by_id(template_id, request=request)
    # get namespaces
    namespaces = get_namespaces(template.content)
    # get default prefix
    default_prefix = get_default_prefix(namespaces)

    query = dict()
    for field in form_values:
        bool_comp = field["operator"]
        is_not = bool_comp == "NOT"
        element_type = field.get("type", None)

        # get element value
        value = get_element_value(field)
        # get comparison operator
        comparison = get_element_comparison(field)

        element_id = field["id"]

        if element_type == "query":
            try:
                saved_query = saved_query_api.get_by_id(element_id)
            except DoesNotExist:
                raise MongoQueryException("The saved query does not exist anymore.")
            criteria = build_query_criteria(json.loads(saved_query.query), is_not)
        else:
            data_structure_element = data_structure_element_api.get_by_id(
                element_id, request
            )
            element = get_dot_notation_to_element(data_structure_element, namespaces)
            criteria = build_criteria(
                element,
                comparison,
                value,
                element_type,
                default_prefix,
                is_not,
                use_wildcard,
            )

        if bool_comp == "OR":
            query = build_or_criteria(query, criteria)
        elif bool_comp == "AND":
            query = build_and_criteria(query, criteria)
        else:
            if form_values.index(field) == 0:
                query.update(criteria)
            else:
                query = build_and_criteria(query, criteria)

    return query


def sub_elements_to_query(form_values, namespaces, default_prefix, request):
    """Transforms HTML fields in a query on sub-elements

    Args:
        form_values:
        namespaces:
        default_prefix:
        request:

    Returns:

    """
    elem_match = []

    # get the parent path using the first element of the list
    parent_path = get_parent_path(form_values[0]["id"], namespaces, request)

    for i in range(0, len(form_values)):
        field = form_values[i]
        if field["selected"] is True:
            bool_comp = field["operator"]
            if bool_comp == "NOT":
                is_not = True
            else:
                is_not = False

            data_structure_element = data_structure_element_api.get_by_id(
                field["id"], request
            )
            element_type = data_structure_element.options["type"]
            element_name = data_structure_element.options["name"]
            value = get_element_value(field)
            comparison = get_element_comparison(field)

            criteria = build_criteria(
                element_name, comparison, value, element_type, default_prefix, is_not
            )

            elem_match.append(criteria)

    query = {parent_path: {"$elemMatch": {"$and": elem_match}}}

    return query
