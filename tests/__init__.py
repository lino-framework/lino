"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load SETUP_INFO:
execfile(ROOTDIR.child('lino_noi', 'project_info.py'), globals())

from lino.utils.pythontest import TestCase

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_noi.settings.test"


class BaseTestCase(TestCase):
    project_root = ROOTDIR
    django_settings_module = 'lino_noi.settings.test'


class SpecsTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])

    def test_smtpd(self):
        self.run_simple_doctests('docs/specs/smtpd.rst')

    def test_hosts(self):
        self.run_simple_doctests('docs/specs/hosts.rst')

    def test_tickets(self):
        self.run_simple_doctests('docs/specs/tickets.rst')

    def test_clocking(self):
        self.run_simple_doctests('docs/specs/clocking.rst')

    def test_general(self):
        self.run_simple_doctests('docs/specs/general.rst')


class DemoTests(BaseTestCase):
    """Run tests on the demo projects.
    """

    def test_admin(self):
        self.run_django_manage_test()
