""" Settings for core_explore_example_app

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])

PARSER_DOWNLOAD_DEPENDENCIES = getattr(settings, "PARSER_DOWNLOAD_DEPENDENCIES", False)
QUERIES_MAX_DAYS_IN_DATABASE = getattr(settings, "QUERIES_MAX_DAYS_IN_DATABASE", 7)
EXPLORE_EXAMPLE_MENU_NAME = getattr(
    settings, "EXPLORE_EXAMPLE_MENU_NAME", "Query by Example"
)
