"""Utils for the query builder
"""
from django.template.context import Context, RequestContext
from django.template import loader
import json
from os.path import join


# Classes Definition


class BranchInfo:
    """
    Store information about a branch from the xml schema while it is being processed for field selection
    """
    def __init__(self, keep_the_branch=False, selected_leaves=None):
        self.keep_the_branch = keep_the_branch
        self.selected_leaves = selected_leaves if selected_leaves is not None else []

    def add_selected_leaf(self, leaf_id):
        self.selected_leaves.append(leaf_id)
        self.keep_the_branch = True


class ElementInfo:
    """
    Store information about element from the XML schema
    """

    def __init__(self, type="", path=""):
        self.type = type
        self.path = path

    def __to_json__(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class CriteriaInfo:
    """
    Store information about a criteria from the query builder
    """

    def __init__(self, elementInfo=None, queryInfo=None):
        self.elementInfo = elementInfo
        self.queryInfo = queryInfo

    def __to_json__(self):
        json_dict = dict()
        if self.elementInfo is None:
            json_dict["elementInfo"] = None
        else:
            json_dict["elementInfo"] = self.elementInfo.__to_json__()
        if self.queryInfo is None:
            json_dict["queryInfo"] = None
        else:
            json_dict["queryInfo"] = self.queryInfo.__to_json__()
        return json.dumps(json_dict)


class QueryInfo:
    """
    Store information about a query
    """

    def __init__(self, query="", displayed_query=""):
        self.query = query
        self.displayed_query = displayed_query

    def __to_json__(self):
        return json.dumps(self, default=lambda o: o.__dict__)


# Util functions

def prune_html_tree(html_tree):
    """Creates a custom HTML tree from fields chosen by the user

    Args:
        html_tree:

    Returns:

    """
    any_branch_checked = False

    list_li = html_tree.findall("./li")
    for li in list_li:
        branch_info = prune_li(li)
        if branch_info.keep_the_branch:
            any_branch_checked = True

    return any_branch_checked


def prune_ul(ul):
    """Processes the ul element of an HTML list

    Args:
        ul:

    Returns:

    """
    list_li = ul.findall("./li")
    branch_info = BranchInfo()

    for li in list_li:
        li_branch_info = prune_li(li)
        if li_branch_info.keep_the_branch:
            branch_info.keep_the_branch = True
        branch_info.selected_leaves.extend(li_branch_info.selected_leaves)

    checkbox = ul.find("./input[@type='checkbox']")
    if checkbox is not None:
        if 'value' in checkbox.attrib and checkbox.attrib['value'] == 'true':
            # set element class
            parent_li = ul.getparent()
            element_id = parent_li.attrib['class']
            add_selection_attributes(parent_li, 'element', element_id)
            # tells to keep this branch until this leaf
            branch_info.add_selected_leaf(element_id)

    if not branch_info.keep_the_branch:
        add_selection_attributes(ul, 'none')

    return branch_info


def prune_li(li):
    """Processes the li element of an HTML list

    Args:
        li:

    Returns:

    """
    list_ul = li.findall("./ul")
    branch_info = BranchInfo()

    if len(list_ul) != 0:
        selected_leaves = []
        for ul in list_ul:
            ul_branch_info = prune_ul(ul)
            if ul_branch_info.keep_the_branch:
                branch_info.keep_the_branch = True
            selected_leaves.extend(ul_branch_info.selected_leaves)

        # sub element queries available when more than one selected elements under the same element
        if len(selected_leaves) > 1:
            # not for the choices
            if li[0].tag != 'select':
                # TODO: check if test useful
                if 'select_class' not in li.attrib:
                    leaves_id = ' '.join(selected_leaves)
                    add_selection_attributes(li, 'parent', leaves_id)
        if not branch_info.keep_the_branch:
            add_selection_attributes(li, 'none')

        return branch_info
    else:
        try:
            checkbox = li.find("./input[@type='checkbox']")
            if checkbox.attrib['value'] == 'false':
                add_selection_attributes(li, 'none')
                return branch_info
            else:
                element_id = li.attrib['class']
                add_selection_attributes(li, 'element', element_id)
                # tells to keep this branch until this leaf
                branch_info.add_selected_leaf(element_id)
                return branch_info
        except:
            return branch_info


def sub_element_query_li(li, selected_leaves):
    """Updates li with sub-element query attributes

    Args:
        li:
        selected_leaves:

    Returns:

    """
    # not for the choices
    if li[0].tag != 'select':
        # TODO: check if test useful
        if 'select_class' not in li.attrib:
            leaves_id = ' '.join(selected_leaves)
            # set element class
            li.attrib['select_class'] = 'parent'
            li.attrib['select_id'] = leaves_id


def add_selection_attributes(element, select_class, select_id=None):
    """

    Args:
        element:
        select_class:
        select_id:

    Returns:

    """
    element.attrib['select_class'] = select_class
    if select_id is not None:
        element.attrib['select_id'] = select_id


# Rendering functions


def render_yes_or_not():
    """Returns a string that represents an html select with yes or not options

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'yes_no.html'))


def render_and_or_not():
    """Returns a string that represents an html select with AND, OR, NOT options

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'and_or_not.html'))


def render_numeric_select():
    """Returns a string that represents an html select with numeric comparisons

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'numeric_select.html'))


def render_value_input():
    """Returns an input to type a value

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'input.html'))


def render_string_select():
    """Returns an input to type a value

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'string_select.html'))


def render_initial_form():
    """Renders the initial Query Builder

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'initial_form.html'))


def render_remove_button():
    """Returns html of a remove button

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'remove.html'))


def render_add_button():
    """Returns html of an add button

    Returns:

    """
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'add.html'))


def render_enum(request, enums):
    """Returns html select from an enumeration

    Args:
        request:
        enums:

    Returns:

    """
    context = RequestContext(request, {
        'enums': enums,
    })
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'enum.html'), context)


def render_new_query(tag_id, query, is_first=False):
    """Returns an html string for a new query

    Args:
        tag_id:
        query:
        is_first:

    Returns:

    """
    context = Context({
        'tagID': tag_id,
        'query': query,
        'first': is_first
    })
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'new_query.html'), context)


def render_new_criteria(tag_id):
    """Returns an html string for a new query

    Args:
        tag_id:

    Returns:

    """
    context = Context({
        'tagID': tag_id,
    })
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'new_criteria.html'), context)


def render_sub_elements_query(parent_name, form_fields):
    """Returns an html string for a query on sub-elements

    Args:


    Returns:

    """
    context = Context({
        'parent_name': parent_name,
        'form_fields': form_fields,
    })
    return _render_template(join('core_explore_example_app', 'user', 'query_builder', 'sub_elements_query.html'),
                            context)


def get_element_value(element_field):
    """Get value from field

    Args:
        element_field:

    Returns:

    """
    return element_field['value'] if 'value' in element_field else None


def get_element_comparison(element_field):
    """Get comparison operator from field

    Args:
        element_field:

    Returns:

    """
    return element_field['comparison'] if 'comparison' in element_field else None


def _render_template(template_path, context=None):
    """Returns an HTML string rendered from the template

    Args:
        template_path:

    Returns:

    """
    if context is None:
        context = Context()
    template = loader.get_template(template_path)
    return template.render(context)
