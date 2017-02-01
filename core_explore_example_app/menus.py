""" Add Explore Example in main menu
"""

from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "main", MenuItem("Query by Example", reverse("core_explore_example_index"))
)
