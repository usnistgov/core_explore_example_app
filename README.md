# core_explore_example_app

core_explore_example_app is a Django app.

# Quick start

1. Add "core_explore_example_app" to your INSTALLED_APPS setting like this:

  ```python
  INSTALLED_APPS = [
      ...
      'core_explore_example_app',
  ]
  ```

  2. Include the core_explore_example_app URLconf in your project urls.py like this::

  ```python
  url(r'^explore/example/', include('core_explore_example_app.urls')),
  ```

