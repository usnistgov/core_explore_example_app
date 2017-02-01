"""Parser util for explore app
"""
from core_parser_app.tools.parser.parser import XSDParser
from core_parser_app.tools.parser.renderer.checkbox import CheckboxRenderer
from core_parser_app.components.data_structure_element import api as data_structure_element_api


def get_parser():
    """Returns parser

    Returns:

    """

    return XSDParser(min_tree=False,
                     ignore_modules=True,
                     collapse=True,
                     auto_key_keyref=False,
                     implicit_extension_base=False,
                     download_dependencies=False,
                     store_type=True)


# FIXME: refactor common code with core curate app (note: no xml_string here)
def generate_form(request, xsd_string):
    """Generates the form using the parser, returns the root element

    Args:
        request:
        xsd_string:

    Returns:

    """
    # build parser
    parser = get_parser()
    # generate form
    root_element_id = parser.generate_form(request, xsd_string)
    # get the root element
    root_element = data_structure_element_api.get_by_id(root_element_id)

    return root_element


def render_form(request, root_element):
    """Renders the form

    Args:
        request:
        root_element:

    Returns:

    """
    # build a renderer
    renderer = CheckboxRenderer(root_element, request)
    # render the form
    xsd_form = renderer.render()

    return xsd_form
