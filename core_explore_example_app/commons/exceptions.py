""" Core Explore Example exceptions
"""


class MongoQueryException(Exception):
    """
    Exception raised by mongo query builder
    """

    def __init__(self, message):
        self.message = message
