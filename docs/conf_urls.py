""" Conf urls
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

from core_explore_example_app import urls as core_explore_example_app_urls

urlpatterns = [
    re_path(r"^admin/", include(admin.site.urls)),
] + core_explore_example_app_urls.urlpatterns
