""" Fixtures files for Data
"""

from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class DataFixtures(FixtureInterface):
    """Data fixtures"""

    user_xsd_template = None
    user_json_template = None
    user_template_vm_xsd = None
    user_template_vm_json = None
    global_xsd_template = None
    global_json_template = None
    global_template_vm_xsd = None
    global_template_vm_json = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_templates()

    def generate_templates(self):
        """Generate Templates.

        Returns:

        """
        self.user_template_vm_xsd = TemplateVersionManager(
            title="user template XSD",
            user="1",
            is_disabled=False,
        )
        self.user_template_vm_xsd.save_version_manager()

        self.user_xsd_template = Template(
            content=(
                '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
                '<xs:element name="tag"></xs:element></xs:schema>'
            ),
            hash="",
            format=Template.XSD,
            filename="filename.xsd",
            version_manager=self.user_template_vm_xsd,
        )
        self.user_xsd_template.save()

        self.user_template_vm_json = TemplateVersionManager(
            title="user template JSON",
            user="1",
            is_disabled=False,
        )
        self.user_template_vm_json.save_version_manager()

        self.user_json_template = Template(
            content="{}",
            hash="",
            format=Template.JSON,
            filename="filename.json",
            version_manager=self.user_template_vm_json,
        )
        self.user_json_template.save()

        self.global_template_vm_xsd = TemplateVersionManager(
            title="global template XSD",
            user=None,
            is_disabled=False,
        )
        self.global_template_vm_xsd.save_version_manager()

        self.global_xsd_template = Template(
            content=(
                '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
                '<xs:element name="tag"></xs:element></xs:schema>'
            ),
            hash="",
            format=Template.XSD,
            filename="filename.xsd",
            version_manager=self.global_template_vm_xsd,
        )
        self.global_xsd_template.save()

        self.global_template_vm_json = TemplateVersionManager(
            title="global template JSON",
            user=None,
            is_disabled=False,
        )
        self.global_template_vm_json.save_version_manager()

        self.global_json_template = Template(
            content="{}",
            hash="",
            format=Template.JSON,
            filename="filename.json",
            version_manager=self.global_template_vm_json,
        )
        self.global_json_template.save()
