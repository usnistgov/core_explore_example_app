"""Util to build queries for mongo db
"""
from bson.objectid import ObjectId
import copy
import json
import re

from core_explore_example_app.utils.xml import get_list_xsd_numbers, get_list_xsd_floating_numbers
from core_main_app.components.data import api as data_api
from core_parser_app.components.data_structure_element import api as data_structure_element_api


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
        criteria[path] = json.loads('{{"${0}": {1} }}'.format(comparison, value))

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
        criteria[path] = json.loads('{{"${0}": {1} }}'.format(comparison, value))

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


def build_enum_criteria(path, value, is_not=False):
    """Builds a criteria for an enumeration

    Args:
        path:
        value:
        is_not:

    Returns:

    """
    criteria = dict()

    if is_not:
        criteria[path] = json.loads('{{"ne": "{0}" }}'.format(repr(value)))
    else:
        criteria[path] = value

    return criteria


def build_and_criteria(criteria1, criteria2):
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


def build_or_criteria(criteria1, criteria2):
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


def build_criteria(element_path, comparison, value, element_type, default_prefix, is_not=False):
    """Looks at element type and route to the right function to build the criteria

    Args:
        element_path:
        comparison:
        value:
        element_type:
        default_prefix:
        is_not:

    Returns:

    """
    # build the query: value can be found at element:value or at element.#text:value
    # second case appends when the element has attributes or namespace information
    if element_type in get_list_xsd_numbers(default_prefix):
        element_query = build_int_criteria(element_path, comparison, value)
        attribute_query = build_int_criteria("{}.#text".format(element_path), comparison, value)
    elif element_type in get_list_xsd_floating_numbers(default_prefix):
        element_query = build_float_criteria(element_path, comparison, value)
        attribute_query = build_float_criteria("{}.#text".format(element_path), comparison, value)
    else:
        element_query = build_string_criteria(element_path, comparison, value)
        attribute_query = build_string_criteria("{}.#text".format(element_path), comparison, value)

    criteria = build_or_criteria(element_query, attribute_query)

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
    for key, value in query.iteritems():
        if key == "$and" or key == "$or":
            # invert the query for the case value can be found at element:value or at element.#text:value
            # second case appends when the element has attributes or namespace information
            if len(value) == 2 and len(value[0].keys()) == 1 and len(value[1].keys()) == 1 and \
                            value[1].keys()[0] == "{}.#text".format(value[0].keys()[0]):
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
                if value.keys()[0] == "$not" or value.keys()[0] == "$ne":
                    query[key] = (value[value.keys()[0]])
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
    if isinstance(expr, re._pattern_type):
        return True
    try:
        if expr.startswith('/') and expr.endswith('/'):
            return True
        else:
            return False
    except:
        return False


def xpath_to_dot_notation(xpath, namespaces):
    """Transforms XML xpath into dot notation

    Args:
        xpath:
        namespaces:

    Returns:

    """
    # remove indexes from xpath
    xpath = re.sub(r'\[[0-9]+\]', '', xpath)
    # remove namespaces
    for prefix in namespaces.keys():
        xpath = re.sub(r'{}:'.format(prefix), '', xpath)
    # replace / by .
    xpath = xpath.replace("/", ".")

    return xpath[1:]


def get_dot_notation_to_element(data_structure_element, namespaces):
    """

    Args:
        data_structure_element:
        namespaces:

    Returns:

    """
    # get data structure element's xml xpath
    xml_xpath = data_structure_element.options['xpath']['xml']
    # transform xml xpath to dot notation
    dot_notation = xpath_to_dot_notation(xml_xpath, namespaces)

    return dot_notation


def get_parent_name(data_structure_element_id, namespaces):
    """

    Args:
        data_structure_element_id:
        namespaces:

    Returns:

    """
    # get the data structure element
    data_structure_element = data_structure_element_api.get_by_id(data_structure_element_id)
    # convert xml path to mongo dot notation
    data_structure_element_dot_notation = get_dot_notation_to_element(data_structure_element, namespaces)
    # get parent name
    parent_name = data_structure_element_dot_notation.split(".")[-2]

    return parent_name


def get_parent_path(data_structure_element_id, namespaces):
    """

    Args:
        data_structure_element_id:
        namespaces:

    Returns:

    """
    # get the data structure element
    data_structure_element = data_structure_element_api.get_by_id(data_structure_element_id)
    # convert xml path to mongo dot notation
    data_structure_element_dot_notation = get_dot_notation_to_element(data_structure_element, namespaces)
    # get path to parent element
    parent_path = ".".join(data_structure_element_dot_notation.split(".")[:-1])

    return parent_path

