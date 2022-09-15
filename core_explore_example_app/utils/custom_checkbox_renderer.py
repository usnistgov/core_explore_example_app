"""Custom Checkbox Renderer class
"""
from core_parser_app.tools.parser.renderer.checkbox import CheckboxRenderer


class CustomCheckboxRenderer(CheckboxRenderer):
    """Custom Checkbox renderer, makes elements selectable and allows only one occurrence of each element"""

    def render_element(self, element):
        """render_element
        Args:
            element:

        Returns:
        """
        return super().render_element(_restrict_occurs(element))

    def render_attribute(self, element):
        """render_attribute
        Args:
            element:

        Returns:
        """
        return super().render_attribute(_restrict_occurs(element))

    def render_sequence(self, element, force_full_display=False):
        """render_sequence
        Args:
            element:
            force_full_display:

        Returns:
        """
        return super().render_sequence(
            _restrict_occurs(element), force_full_display=force_full_display
        )

    def render_choice(self, element):
        """render_choice
        Args:
            element:

        Returns:
        """
        return super().render_choice(_restrict_occurs(element))


def _restrict_occurs(element):
    """Restrict the number of occurrences to 1

    Args:
        element:

    Returns:

    """
    # if min number of occurrences is set
    if "min" in element.options:
        # if more than one occurrence
        if element.options["min"] > 1:
            # keep only first element of the list
            element.children.set([element.children.all()[0]])
            # force min occurrences to one
            element.options["min"] = 1
    # force max number of occurrences to one
    element.options["max"] = 1
    # return element
    return element
