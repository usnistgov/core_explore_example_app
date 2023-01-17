""" Explore Common App tasks
"""
import logging

from celery import shared_task

from core_explore_example_app.settings import QUERIES_MAX_DAYS_IN_DATABASE
from core_explore_example_app.system.api import (
    get_saved_queries_created_by_app,
)
from core_main_app.utils.datetime import datetime_now, datetime_timedelta

logger = logging.getLogger(__name__)


@shared_task
def delete_temporary_saved_queries():
    """Every day at midnight, delete older temporary saved queries.

    Returns:

    """
    try:
        # get older queries
        old_queries = [
            query
            for query in get_saved_queries_created_by_app()
            if query.creation_date
            < datetime_now()
            - datetime_timedelta(days=QUERIES_MAX_DAYS_IN_DATABASE)
        ]
        # remove old queries from database
        for query in old_queries:
            logger.info("Periodic task: delete saved query %s.", str(query.id))
            query.delete()
    except Exception as exception:
        logger.error(
            "An error occurred while deleting temporary saved queries (%s).",
            str(exception),
        )
