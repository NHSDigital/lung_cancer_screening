
import os

from django.test import TestCase, override_settings, tag
from unittest.mock import patch

from lung_cancer_screening.jinja2_env import get_env_value

@tag("Jinja2Env")
class TestJinja2Env(TestCase):
    def test_get_env_value_with_env(self):
        # Test with an environment variable
        with patch.dict(os.environ, {"TEST_ENV_VAR": "env_value"}, clear=False):
            self.assertEqual(get_env_value("TEST_ENV_VAR"), "env_value")
    @override_settings(TEST_SETTING="setting_value")
    def test_get_env_value_with_setting(self):
        # Test with a Django setting
        self.assertEqual(get_env_value('TEST_SETTING'), 'setting_value')

    def test_get_env_value_without_a_value(self):
        # Test with a non-existent key
        self.assertEqual(get_env_value('NON_EXISTENT_KEY'), 'Value not found')

    @override_settings(TEST_BOTH="setting_value")
    def test_get_env_value_with_env_with_both(self):
        # Test environment variable takes precedence over Django setting
        with patch.dict(os.environ, {"TEST_BOTH": "env_value"}, clear=False):
            self.assertEqual(get_env_value("TEST_BOTH"), "env_value")


