from django.test import TestCase, override_settings
from django.utils.translation import gettext_lazy, override

from wagtail_honeypot.models import HoneypotFormMixin


class TestHoneypotFormMixinLocale(TestCase):
    """
    Test the locale/translation support of HoneypotFormMixin
    """

    def test_honeypot_field_verbose_name_is_translatable(self):
        """
        Test that the honeypot field's verbose_name is a lazy translation object
        """
        field = HoneypotFormMixin._meta.get_field("honeypot")
        self.assertIsInstance(field.verbose_name, type(gettext_lazy("test")))

    def test_honeypot_field_verbose_name_default(self):
        """
        Test that the honeypot field's verbose_name is set correctly in English
        """
        field = HoneypotFormMixin._meta.get_field("honeypot")
        # Convert lazy translation to string to check content
        self.assertEqual(str(field.verbose_name), "Honeypot enabled")

    @override_settings(LANGUAGE_CODE="fr")
    def test_honeypot_field_verbose_name_french_locale(self):
        """
        Test that the honeypot field's verbose_name can be translated to French
        """
        with override("fr"):
            field = HoneypotFormMixin._meta.get_field("honeypot")
            # The verbose_name should still be available for translation
            verbose_name = str(field.verbose_name)
            self.assertIsNotNone(verbose_name)
            self.assertTrue(len(verbose_name) > 0)
