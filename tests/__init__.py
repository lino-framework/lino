import sys
from unipath import Path

from lino.utils.pythontest import TestCase
from lino import SETUP_INFO


class LinoTestCase(TestCase):
    django_settings_module = 'lino.projects.std.settings_test'
    project_root = Path(__file__).parent.parent


class PackagesTests(LinoTestCase):
    def test_01(self):
        self.run_packages_test(SETUP_INFO['packages'])


