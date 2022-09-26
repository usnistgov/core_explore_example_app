""" Fixtures files for Persistent Query Example
"""
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_explore_example_app.components.persistent_query_example.models import (
    PersistentQueryExample,
)


class PersistentQueryExampleFixtures(FixtureInterface):
    """Persistent query example fixtures"""

    template = None
    persistent_query_example_1 = None
    persistent_query_example_2 = None
    persistent_query_example_3 = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_query_collection()

    def generate_template(self):
        """generate_template"""

        self.template = Template(
            filename="filename", content="<xml />", hash="hash"
        )
        self.template.save()

    def generate_query_collection(self):
        """Generate a Persistent query example collection.

        Returns:

        """

        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.persistent_query_example_1 = PersistentQueryExample(
            user_id="1", name="persistent_query_example_1"
        )
        self.persistent_query_example_1.save()

        self.persistent_query_example_2 = PersistentQueryExample(
            user_id="2", name="persistent_query_example_2"
        )
        self.persistent_query_example_2.save()

        self.persistent_query_example_3 = PersistentQueryExample(
            user_id="3", name="persistent_query_example_3"
        )
        self.persistent_query_example_3.save()

        self.data_collection = [
            self.persistent_query_example_1,
            self.persistent_query_example_2,
            self.persistent_query_example_3,
        ]
