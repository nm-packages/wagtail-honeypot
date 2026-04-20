from bs4 import BeautifulSoup as bs4
from django.template import Context, Template
from django.test import TestCase, override_settings

from wagtail_honeypot.templatetags.honeypot_tags import honeypot_fields


class TestHoneypotTemplateTags(TestCase):
    """
    Test the honeypot template tags
    """

    def assert_honeypot_input(self, soup, *, field_id, field_name, field_type):
        input_field = soup.find("input", {"id": field_id, "name": field_name, "type": field_type})
        self.assertIsNotNone(input_field)
        self.assertEqual(input_field.get("tabindex"), "-1")
        self.assertEqual(input_field.get("autocomplete"), "off")
        self.assertEqual(input_field.get("aria-hidden"), "true")
        return input_field

    def test_honeypot_template_tag_context_enabled(self):
        """
        Test that the honeypot template tag returns the correct data
        when the honeypot is enabled
        """
        fields_data = honeypot_fields(True)
        self.assertEqual(fields_data["honeypot_name_field"], "whf_name")
        self.assertEqual(fields_data["honeypot_time_field"], "whf_time")
        self.assertIsInstance(int(fields_data["time"]), int)
        self.assertTrue(fields_data["enabled"])

    def test_honeypot_template_tag_context_disabled(self):
        """
        Test that the honeypot template tag returns the correct data
        when the honeypot is disabled
        """
        fields_data = honeypot_fields(False)
        self.assertFalse(fields_data["enabled"])

    def test_honeypot_tags_rendered(self):
        """
        Test that the honeypot template tag renders the correct HTML
        when the honeypot is enabled
        """
        context = Context({"honeypot": True})
        template = Template("{% load honeypot_tags %}{% honeypot_fields honeypot %}")

        soup = bs4(template.render(context), "html.parser")

        self.assert_honeypot_input(soup, field_id="whf_name", field_name="whf_name", field_type="text")
        self.assert_honeypot_input(soup, field_id="whf_time", field_name="whf_time", field_type="hidden")

    @override_settings(HONEYPOT_NAME_FIELD="foo", HONEYPOT_TIME_FIELD="bar")
    def test_honeypot_tags_override_field_names(self):
        """
        Test that the honeypot template tag renders the correct HTML
        when the honeypot is enabled and the field names are overridden
        """
        context = Context({"honeypot": True})
        template = Template("{% load honeypot_tags %}{% honeypot_fields honeypot %}")

        soup = bs4(template.render(context), "html.parser")

        self.assert_honeypot_input(soup, field_id="foo", field_name="foo", field_type="text")
        self.assert_honeypot_input(soup, field_id="bar", field_name="bar", field_type="hidden")
