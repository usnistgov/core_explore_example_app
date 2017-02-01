"""Util to build user readable queries
"""


def build_pretty_criteria(element_name, comparison, value, is_not=False):
    """Returns a pretty representation of the criteria

    Args:
        element_name:
        comparison:
        value:
        is_not:

    Returns:

    """
    pretty_criteria = ""

    if is_not:
        pretty_criteria += "NOT("

    pretty_criteria += element_name

    if comparison == "lt":
        pretty_criteria += " &lt; "
    elif comparison == "lte":
        pretty_criteria += " &le; "
    elif comparison == "=":
        pretty_criteria += "="
    elif comparison == "gte":
        pretty_criteria += " &ge; "
    elif comparison == "gt":
        pretty_criteria += " &gt; "
    elif comparison == "is":
        pretty_criteria += " is "
    elif comparison == "like":
        pretty_criteria += " like "

    if value == "":
        pretty_criteria += ' &ldquo;  &ldquo;'
    else:
        pretty_criteria += value

    if is_not:
        pretty_criteria += ")"

    return pretty_criteria


def build_query_pretty_criteria(query_value, is_not):
    """Returns a pretty representation of the query

    Args:
        query_value:
        is_not:

    Returns:

    """
    if is_not:
        return "NOT(" + query_value + ")"
    else:
        return query_value


def build_enum_pretty_criteria(element, value, is_not=False):
    """Returns a pretty representation of the enumeration value

    Args:
        element:
        value:
        is_not:

    Returns:

    """
    if (is_not):
        return "NOT(" + str(element) + " is " + str(value) + ")"
    else:
        return element + " is " + value


def build_or_pretty_criteria(query, criteria):
    """Returns a pretty representation of the OR

    Args:
        query:
        criteria:

    Returns:

    """
    return "(" + query + " OR " + criteria + ")"


def build_and_pretty_criteria(query, criteria):
    """Returns a pretty representation of the AND

    Args:
        query:
        criteria:

    Returns:

    """
    return "(" + query + " AND " + criteria + ")"
