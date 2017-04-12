"""Explore Example app Ajax views
"""
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from lxml import html
import json

from core_explore_common_app.components.query import api as query_api
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_main_app.components.template import api as template_api

from core_explore_example_app.components.saved_query.models import SavedQuery
from core_explore_example_app.components.saved_query import api as saved_query_api
from core_explore_example_app.utils.displayed_query import build_query_pretty_criteria, build_enum_pretty_criteria, \
    build_pretty_criteria, build_or_pretty_criteria, build_and_pretty_criteria
from core_explore_example_app.utils.mongo_query import build_query_criteria, build_enum_criteria, build_criteria, \
    build_or_criteria, build_and_criteria, get_dot_notation_to_element, get_parent_name, get_parent_path
from core_explore_example_app.utils.query_builder import render_numeric_select, render_value_input, \
    render_string_select, render_enum, render_initial_form, CriteriaInfo, ElementInfo, QueryInfo, \
    render_new_query, render_new_criteria, render_sub_elements_query, get_element_value, get_element_comparison, \
    prune_html_tree
from core_explore_example_app.utils.xml import validate_element_value, get_enumerations

from xml_utils.xsd_tree.operations.namespaces import get_namespaces, get_default_prefix
from xml_utils.xsd_types.xsd_types import get_xsd_numbers


# FIXME: avoid session variables


def save_fields(request):
    """Saves the fields selected by the user

    Args:
        request:

    Returns:

    """

    # get form content from HTML
    form_content = request.POST['formContent']
    request.session['formStringExplore'] = form_content

    # modify the form string to only keep the selected elements
    html_tree = html.fromstring(form_content)
    any_checked = prune_html_tree(html_tree)

    if any_checked:
        # if elements selected in the form, set the pruned form in session variable
        request.session['customFormStringExplore'] = html.tostring(html_tree)
    else:
        # if no elements selected in the form, empty session variable
        request.session['customFormStringExplore'] = ""

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def select_element(request):
    """Select an element in the custom tree

    Args:
        request:

    Returns:

    """
    # get element id
    element_id = request.POST['elementID']
    criteria_id = request.POST['criteriaID']

    # get schema element
    schema_element = data_structure_element_api.get_by_id(element_id)

    response_dict = {
        "criteriaTagID": criteria_id,
        "criteriaID": str(criteria_id[4:]),
        "elementName": schema_element.options['label']
    }

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def get_sub_elements_query_builder(request):
    """Build the form for queries on sub elements

    Args:
        request:

    Returns:

    """
    leaves_id = request.POST['leavesID']
    template_id = request.POST['templateID']

    # get list of ids from string
    list_leaves_id = leaves_id.split(" ")

    # get template
    template = template_api.get(template_id)

    # get template namespaces
    namespaces = get_namespaces(template.content)
    # get default prefix
    default_prefix = get_default_prefix(namespaces)

    # get the parent name using the first schema element of the list
    parent_name = get_parent_name(list_leaves_id[0], namespaces)

    form_fields = []
    for leaf_id in list_leaves_id:
        data_structure_element = data_structure_element_api.get_by_id(leaf_id)
        element_type = data_structure_element.options['type']
        element_name = data_structure_element.options['name']

        try:
            if element_type.startswith("{0}:".format(default_prefix)):
                # numeric
                if element_type in get_xsd_numbers(default_prefix):
                    sub_element_field = render_numeric_select() + render_value_input()
                else:
                    sub_element_field = render_string_select() + render_value_input()
            else:
                # enumeration
                enums = get_enumerations(data_structure_element)
                sub_element_field = render_enum(request, enums)
        except:
            sub_element_field = render_string_select() + render_value_input()
        form_fields.append({'element_name': element_name, 'html': sub_element_field})

    response_dict = {'subElementQueryBuilder': render_sub_elements_query(parent_name, form_fields)}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def insert_sub_elements_query(request):
    """Inserts a query for a sub element in the query builder

    Args:
        request:

    Returns:

    """

    form_values = json.loads(request.POST['formValues'])
    leaves_id = request.POST['leavesID']
    template_id = request.POST['templateID']
    criteria_id = request.POST['criteriaID']

    # get list of leaves from string
    list_leaves_id = leaves_id.split(" ")

    map_criteria = request.session['mapCriteriaExplore']

    # get template
    template = template_api.get(template_id)

    # get template namespaces
    namespaces = get_namespaces(template.content)
    # get default prefix
    default_prefix = get_default_prefix(namespaces)

    errors = []
    for i in range(0, len(form_values)):
        field = form_values[i]
        if field['selected'] is True:
            data_structure_element = data_structure_element_api.get_by_id(list_leaves_id[i])
            element_type = data_structure_element.options['type']
            element_name = data_structure_element.options['name']
            element_value = get_element_value(field)

            error = validate_element_value(element_name, element_type, element_value, default_prefix)
            if error is not None:
                errors.append(error)

    if len(errors) == 0:
        query = sub_elements_to_query(form_values, list_leaves_id, namespaces, default_prefix)
        displayed_query = sub_elements_to_pretty_query(form_values, list_leaves_id, namespaces, default_prefix)
        criteria_info = CriteriaInfo()
        criteria_info.queryInfo = QueryInfo(query, displayed_query)
        criteria_info.elementInfo = ElementInfo("query")
        map_criteria[criteria_id] = criteria_info.__to_json__()
        request.session['mapCriteriaExplore'] = map_criteria
        ui_id = "ui" + criteria_id[4:]
        response_dict = {'criteriaID': criteria_id,
                         'prettyQuery': displayed_query,
                         'uiID': ui_id}
    else:
        return HttpResponseBadRequest("<br/>".join(errors), content_type='application/javascript')

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def sub_elements_to_query(form_values, list_leaves_id, namespaces, default_prefix):
    """Transforms HTML fields in a query on sub-elements

    Args:
        form_values:
        list_leaves_id:
        namespaces:
        default_prefix:

    Returns:

    """
    elem_match = {}
    i = 0

    # get the parent path using the first element of the list
    parent_path = get_parent_path(list_leaves_id[0], namespaces)

    for field in form_values:
        if field['selected'] is True:
            bool_comp = field['operator']
            if bool_comp == 'NOT':
                is_not = True
            else:
                is_not = False

            data_structure_element = data_structure_element_api.get_by_id(list_leaves_id[i])
            element_type = data_structure_element.options['type']
            element_name = data_structure_element.options['name']
            value = get_element_value(field)
            comparison = get_element_comparison(field)

            try:
                if element_type.startswith("{0}:".format(default_prefix)):
                    criteria = build_criteria(element_name, comparison, value, element_type, default_prefix, is_not)
                else:
                    criteria = build_enum_criteria(element_name, value, is_not)
            except:
                criteria = build_criteria(element_name, comparison, value, element_type, default_prefix, is_not)

            elem_match.update(criteria)

    query = {parent_path: {"$elemMatch": elem_match}}

    return query


def sub_elements_to_pretty_query(form_values, list_leaves_id, namespaces, default_prefix):
    """Transforms HTML fields in a user readable query

    Args:
        form_values:
        list_leaves_id:
        namespaces:
        default_prefix:

    Returns:

    """
    # get the parent path using the first element of the list
    parent_name = get_parent_name(list_leaves_id[0], namespaces)

    list_criteria = []
    for i in range(0, len(form_values)):
        field = form_values[i]
        if field['selected'] is True:
            bool_comp = field['operator']
            if bool_comp == 'NOT':
                is_not = True
            else:
                is_not = False

            data_structure_element = data_structure_element_api.get_by_id(list_leaves_id[i])
            element_type = data_structure_element.options['type']
            element_name = data_structure_element.options['name']
            value = get_element_value(field)
            comparison = get_element_comparison(field)

            try:
                if element_type.startswith("{0}:".format(default_prefix)):
                    criteria = build_pretty_criteria(element_name, comparison, value, is_not)
                else:
                    criteria = build_enum_pretty_criteria(element_name, value, is_not)
            except:
                criteria = build_pretty_criteria(element_name, comparison, value, is_not)

            list_criteria.append(criteria)

    query = "{0}({1})".format(parent_name, ", ".join(list_criteria))

    return query


def update_user_input(request):
    """Updates the user input of the query builder according to the type of the selected element

    Args:
        request:

    Returns:

    """
    from_element_id = request.POST['fromElementID']
    criteria_id = request.POST['criteriaID']
    template_id = request.POST['templateID']

    map_criteria = request.session['mapCriteriaExplore']

    to_criteria_id = "crit" + str(criteria_id)

    criteria_info = CriteriaInfo()

    # get schema element
    data_structure_element = data_structure_element_api.get_by_id(from_element_id)
    # get template
    template = template_api.get(template_id)

    # convert xml path to mongo dot notation
    namespaces = get_namespaces(template.content)
    default_prefix = get_default_prefix(namespaces)
    dot_notation = get_dot_notation_to_element(data_structure_element, namespaces)

    element_type = data_structure_element.options['type']
    try:
        if element_type.startswith("{0}:".format(default_prefix)):
            # numeric
            if element_type in get_xsd_numbers(default_prefix):
                user_inputs = render_numeric_select() + render_value_input()
            # string
            else:
                user_inputs = render_string_select() + render_value_input()
        else:
            # enumeration
            element_type = 'enum'
            enums = get_enumerations(data_structure_element)
            user_inputs = render_enum(request, enums)
    except:
        # default renders string form
        element_type = "{}:string".format(default_prefix)
        user_inputs = render_string_select() + render_value_input()

    criteria_info.elementInfo = ElementInfo(path=dot_notation, type=element_type)
    map_criteria[to_criteria_id] = criteria_info.__to_json__()
    request.session['mapCriteriaExplore'] = map_criteria

    response_dict = {'userInputs': user_inputs}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def add_criteria(request):
    """Adds an empty criteria to the query builder

    Args:
        request:

    Returns:

    """
    tag_id = request.POST['tagID']
    new_criteria_html = render_new_criteria(tag_id)

    response_dict = {'criteria': new_criteria_html}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def remove_criteria(request):
    """Removes a criteria from the query builder

    Args:
        request:

    Returns:

    """
    criteria_id = request.POST['criteriaID']
    try:
        # remove criteria from list of criteria
        map_criteria = request.session['mapCriteriaExplore']
        del map_criteria[criteria_id]
        request.session['mapCriteriaExplore'] = map_criteria
    except:
        pass

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def save_query(request):
    """Saves a query and updates the html display

    Args:
        request:

    Returns:

    """
    form_values = json.loads(request.POST['formValues'])
    template_id = request.POST['templateID']

    # Check that the user can save a query
    errors = []
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
    else:
        error = 'You have to login to save a query.'
        return HttpResponseBadRequest(error, content_type='application/javascript')

    # Check that the query is valid
    errors = check_query_form(request, form_values, template_id)
    if len(errors) == 0:
        query = fields_to_query(request, form_values, template_id)
        displayed_query = fields_to_pretty_query(request, form_values)

        # save the query in the data base
        saved_query = SavedQuery(user_id=str(user_id),
                                 template=template_api.get(template_id),
                                 query=json.dumps(query),
                                 displayed_query=displayed_query)
        saved_query_api.upsert(saved_query)
    else:
        return HttpResponseBadRequest(_render_errors(errors), content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def check_query_form(request, form_values, template_id):
    """Checks that values entered by the user match each element type

    Args:
        request:
        form_values:
        template_id:

    Returns:

    """

    map_criteria = request.session['mapCriteriaExplore']

    template = template_api.get(template_id)
    namespaces = get_namespaces(template.content)
    default_prefix = get_default_prefix(namespaces)

    # check if there are no errors in the query
    errors = []
    if len(map_criteria) != len(form_values) or len(map_criteria) == 0:
        errors.append("Some fields are empty.")
    else:
        for field in form_values:
            criteria_info = json.loads(map_criteria[field['id']])
            element_info = json.loads(criteria_info['elementInfo'])
            element_type = element_info['type']
            element_path = element_info['path']
            element_name = element_path.split('.')[-1]
            element_value = get_element_value(field)
            error = validate_element_value(element_name, element_type, element_value, default_prefix)
            if error is not None:
                errors.append(error)

    return errors


def fields_to_query(request, form_values, template_id):
    """Takes values from the html tree and creates a query from them

    Args:
        request:
        form_values:
        template_id:

    Returns:

    """

    map_criteria = request.session['mapCriteriaExplore']

    query = dict()
    for field in form_values:
        bool_comp = field['operator']
        if bool_comp == 'NOT':
            is_not = True
        else:
            is_not = False

        # get element value
        value = get_element_value(field)
        # get comparison operator
        comparison = get_element_comparison(field)

        # get data structures for query
        criteria_info = json.loads(map_criteria[field['id']])
        element_info = json.loads(criteria_info['elementInfo']) if criteria_info['elementInfo'] is not None else None
        query_info = json.loads(criteria_info['queryInfo']) if criteria_info['queryInfo'] is not None else None

        element_type = element_info['type']
        if element_type == "query":
            query_value = query_info['query']
            criteria = build_query_criteria(query_value, is_not)
        elif element_type == "enum":
            element = element_info['path']
            criteria = build_enum_criteria(element, value, is_not)
        else:
            element = element_info['path']
            template = template_api.get(template_id)
            namespaces = get_namespaces(template.content)
            default_prefix = get_default_prefix(namespaces)
            criteria = build_criteria(element, comparison, value, element_type, default_prefix, is_not)

        if bool_comp == 'OR':
            query = build_or_criteria(query, criteria)
        elif bool_comp == 'AND':
            query = build_and_criteria(query, criteria)
        else:
            if form_values.index(field) == 0:
                query.update(criteria)
            else:
                query = build_and_criteria(query, criteria)

    return query


def fields_to_pretty_query(request, form_values):
    """Transforms fields from the HTML form into pretty representation

    Args:
        request:
        form_values:

    Returns:

    """

    map_criteria = request.session['mapCriteriaExplore']

    query = ""

    for field in form_values:
        bool_comp = field['operator']
        if bool_comp == 'NOT':
            is_not = True
        else:
            is_not = False

        # get element value
        value = get_element_value(field)
        # get comparison operator
        comparison = get_element_comparison(field)

        # get data structures for query
        criteria_info = json.loads(map_criteria[field['id']])
        element_info = json.loads(criteria_info['elementInfo']) if criteria_info['elementInfo'] is not None else None
        query_info = json.loads(criteria_info['queryInfo']) if criteria_info['queryInfo'] is not None else None

        element_type = element_info['type']
        if element_type == "query":
            query_value = query_info['displayed_query']
            criteria = build_query_pretty_criteria(query_value, is_not)
        elif element_type == "enum":
            element_path = element_info['path']
            element = element_path.split('.')[-1]
            criteria = build_enum_pretty_criteria(element, value, is_not)
        else:
            element_path = element_info['path']
            element = element_path.split('.')[-1]
            criteria = build_pretty_criteria(element, comparison, value, is_not)

        if bool_comp == 'OR':
            query = build_or_pretty_criteria(query, criteria)
        elif bool_comp == 'AND':
            query = build_and_pretty_criteria(query, criteria)
        else:
            if form_values.index(field) == 0:
                query += criteria
            else:
                query = build_and_pretty_criteria(query, criteria)

    return query


def _render_errors(errors):
    """Renders a list of errors in a paragraph

    Args:
        errors:

    Returns:

    """
    return '<br/>'.join(errors)


def clear_criteria(request):
    """Clears the Query Builder

    Args:
        request:

    Returns:

    """
    request.session['mapCriteriaExplore'] = dict()
    new_form = render_initial_form()
    response_dict = {'queryForm': new_form}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def clear_queries(request):
    """Deletes all saved queries

    Args:
        request:

    Returns:

    """
    template_id = request.POST['templateID']
    saved_queries = saved_query_api.get_all_by_user_and_template(user_id=str(request.user.id),
                                                                 template_id=template_id)
    for saved_query in saved_queries:
        saved_query_api.delete(saved_query)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def delete_query(request):
    """Deletes a query and update the HTML display

    Args:
        request:

    Returns:

    """
    saved_query_id = request.POST['savedQueryID']
    saved_query = saved_query_api.get_by_id(saved_query_id[5:])
    saved_query_api.delete(saved_query)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def add_query_criteria(request):
    """Adds the selected query to query builder

    Args:
        request:

    Returns:

    """
    tag_id = request.POST['tagID']
    saved_query_id = request.POST['savedQueryID']

    map_criteria = request.session['mapCriteriaExplore']

    # check if first criteria
    is_first = True if len(map_criteria) == 0 else False

    # get saved query number from id
    saved_query_id_number = saved_query_id[5:]
    saved_query = saved_query_api.get_by_id(saved_query_id_number)

    # build criteria id
    criteria_id = 'crit' + str(tag_id)

    # add query to list of criteria
    criteria_info = CriteriaInfo()
    criteria_info.queryInfo = QueryInfo(query=json.loads(saved_query.query),
                                        displayed_query=saved_query.displayed_query)
    criteria_info.elementInfo = ElementInfo("query")
    map_criteria[criteria_id] = criteria_info.__to_json__()

    request.session['mapCriteriaExplore'] = map_criteria

    new_query_html = render_new_query(tag_id, saved_query.displayed_query, is_first)
    response_dict = {'query': new_query_html, 'first': is_first}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def get_query(request):
    """Get a query

    Args:
        request:

    Returns:

    """
    try:
        template_id = request.POST['templateID']
        query_id = request.POST['queryID']
        form_values = json.loads(request.POST['formValues'])

        # save current query builder in session to restore it when coming back to the page
        query_form = request.POST['queryForm']
        request.session['savedQueryFormExplore'] = query_form

        errors = check_query_form(request, form_values, template_id)
        query_object = query_api.get_by_id(query_id)
        if len(query_object.data_sources) == 0:
            errors.append("Please select at least 1 data source.")

        if len(errors) == 0:
            query_content = fields_to_query(request, form_values, template_id)
            query_object.content = json.dumps(query_content)
            query_api.upsert(query_object)
        else:
            return HttpResponseBadRequest(_render_errors(errors), content_type='application/javascript')

        return HttpResponse(json.dumps({}), content_type='application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')
