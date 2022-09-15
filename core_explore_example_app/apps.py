""" Apps file for setting core package when app is ready
"""
import sys

from django.apps import AppConfig

from core_explore_example_app.permissions import discover


class ExploreExampleAppConfig(AppConfig):
    """Core application settings"""

    name = "core_explore_example_app"
    verbose_name = "Core Explore by Example App"

    def ready(self):
        """Runs when the app is ready

        Returns:

        """
        if "migrate" not in sys.argv:
            from core_explore_example_app import discover as app_discover

            app_discover.init_periodic_tasks()
            discover.init_permissions(self.apps)
