========================
Core Explore Example App
========================

Exploration by example for the curator core project.

Quick start
===========

1. Add "core_explore_example_app" to your INSTALLED_APPS setting
----------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_explore_example_app',
    ]

2. Include the core_explore_example_app URLconf in your project urls.py
-----------------------------------------------------------------------

.. code:: python

    url(r'^explore/example/', include('core_explore_example_app.urls')),
