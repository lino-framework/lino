import sys
from unipath import Path

from lino.utils.pythontest import TestCase
from lino import SETUP_INFO
from lino import PYAFTER26
from lino.utils.html2xhtml import HAS_TIDYLIB


class LinoTestCase(TestCase):
    django_settings_module = 'lino.projects.std.settings_test'
    project_root = Path(__file__).parent.parent


class PackagesTests(LinoTestCase):
    def test_01(self):
        self.run_packages_test(SETUP_INFO['packages'])


class CoreTests(TestCase):

    def test_utils(self):
        self.run_simple_doctests('lino/utils/__init__.py')

    def test_site(self):

        # note that run_simple_doctests (i.e. python -m doctest
        # lino/core/site.py) does NOT run any tests in Python 2.7.6
        # because it imports the `site` module of the standard
        # library.

        # self.run_simple_doctests('lino/core/site.py')
        args = [sys.executable]
        args += ['lino/core/site.py']
        self.run_subprocess(args)

    # TODO: implement pseudo tests for QuantityField
    # def test_fields(self):
    #     self.run_simple_doctests('lino/core/fields.py')


class UtilsTests(LinoTestCase):

    def test_instantiator(self):
        self.run_simple_doctests("lino/utils/instantiator.py")

    def test_html2odf(self):
        self.run_simple_doctests('lino/utils/html2odf.py')

    def test_jinja(self):
        self.run_simple_doctests('lino/utils/jinja.py')

    def test_xmlgen_html(self):
        self.run_simple_doctests('lino/utils/xmlgen/html.py')

    def test_html2rst(self):
        self.run_simple_doctests('lino/utils/html2rst.py')

    def test_xmlgen_sepa(self):
        if PYAFTER26:
            self.run_simple_doctests('lino/utils/xmlgen/sepa/__init__.py')

    def test_memo(self):
        self.run_simple_doctests('lino/utils/memo.py')

    def test_tidy(self):
        if HAS_TIDYLIB:
            self.run_simple_doctests('lino/utils/html2xhtml.py')

    def test_demonames(self):
        self.run_simple_doctests("""
        lino/utils/demonames/bel.py
        lino/utils/demonames/est.py
        """)

    def test_odsreader(self):
        self.run_simple_doctests('lino/utils/odsreader.py')
    
    def test_ssin(self):
        self.run_simple_doctests('lino/utils/ssin.py')

    # def test_choicelists(self):
    #     self.run_simple_doctests('lino/core/choicelists.py')

    def test_jsgen(self):
        self.run_simple_doctests('lino/utils/jsgen.py')

    def test_format_date(self):
        self.run_simple_doctests('lino/utils/format_date.py')

    def test_ranges(self):
        self.run_simple_doctests('lino/utils/ranges.py')

    def test_addressable(self):
        self.run_simple_doctests('lino/utils/addressable.py')

    def test_cycler(self):
        self.run_simple_doctests('lino/utils/cycler.py')


