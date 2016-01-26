import sys
from unipath import Path

from lino.utils.pythontest import TestCase
from lino import SETUP_INFO
from lino import PYAFTER26
from lino.utils.html2xhtml import HAS_TIDYLIB


class LinoTestCase(TestCase):
    django_settings_module = "lino.projects.docs.settings.demo"
    project_root = Path(__file__).parent.parent


class PackagesTests(LinoTestCase):
    def test_01(self):
        self.run_packages_test(SETUP_INFO['packages'])


class LibTests(LinoTestCase):

    def test_users(self):
        self.run_simple_doctests("docs/dev/users.rst")

    def test_cal_utils(self):
        self.run_simple_doctests('lino/modlib/cal/utils.py')


class DocsAdminTests(TestCase):
    def test_printing(self):
        self.run_simple_doctests('docs/admin/printing.rst')


class SpecsTests(LinoTestCase):

    def test_holidays(self):
        self.run_simple_doctests('docs/specs/holidays.rst')

class DocsTests(LinoTestCase):

    # python setup.py test -s tests.DocsTests.test_docs
    def test_docs(self):
        self.run_simple_doctests("""
        docs/dev/ml/contacts.rst
        docs/dev/mixins.rst
        docs/user/templates_api.rst
        docs/tested/test_i18n.rst
        """)

    def test_i18n(self):
        self.run_simple_doctests('docs/dev/i18n.rst')

    def test_setup(self):
        self.run_simple_doctests('docs/dev/setup.rst')

    def test_cv(self):
        self.run_simple_doctests('docs/tested/cv.rst')

    def test_households(self):
        self.run_simple_doctests('docs/tested/households.rst')

    def test_gfks(self):
        self.run_simple_doctests('docs/tested/gfks.rst')

    def test_dynamic(self):
        self.run_simple_doctests('docs/tested/dynamic.rst')

    def test_dumpy(self):
        self.run_simple_doctests("docs/tutorials/dumpy.rst")

    def test_polly(self):
        self.run_simple_doctests("docs/tested/polly.rst")

    def test_tinymce(self):
        self.run_simple_doctests("docs/tested/tinymce.rst")

    def test_core_utils(self):
        self.run_simple_doctests("docs/tested/core_utils.rst")

    def test_choicelists(self):
        self.run_simple_doctests("docs/dev/choicelists.rst")

    def test_languages(self):
        self.run_simple_doctests("docs/dev/languages.rst")

    def test_site(self):
        self.run_simple_doctests("docs/dev/site.rst")

    def test_min1(self):
        self.run_simple_doctests("docs/tested/min1.rst")

    def test_e006(self):
        self.run_simple_doctests("docs/tested/e006.rst")

    def test_ddh(self):
        self.run_simple_doctests("docs/tested/ddh.rst")

    def test_settings(self):
        self.run_simple_doctests('docs/dev/ad.rst')

    def test_translate(self):
        self.run_django_manage_test('docs/dev/translate')

    def test_de_BE(self):
        self.run_django_manage_test('docs/tutorials/de_BE')

    def test_sendchanges(self):
        self.run_django_manage_test('docs/tutorials/sendchanges')

    def test_mti(self):
        self.run_django_manage_test('docs/tutorials/mti')

    def test_auto_create(self):
        self.run_django_manage_test('docs/tutorials/auto_create')
    
    def test_human(self):
        self.run_django_manage_test('docs/tutorials/human')

    def test_actions(self):
        self.run_django_manage_test('docs/tutorials/actions')

    def test_actors(self):
        self.run_django_manage_test('docs/tutorials/actors')

    def test_watch(self):
        self.run_django_manage_test('docs/tutorials/watch_tutorial')
    
    def test_vtables(self):
        self.run_django_manage_test('docs/tutorials/vtables')
    
    def test_tables(self):
        self.run_django_manage_test('docs/tutorials/tables')
    
    def test_diamond(self):
        self.run_django_manage_test('docs/tested/diamond')

    def test_diamond2(self):
        self.run_django_manage_test('docs/tested/diamond2')

    def test_addrloc(self):
        self.run_django_manage_test('docs/tutorials/addrloc')
    
    def test_pisa(self):
        self.run_django_manage_test('docs/tutorials/pisa')
    
    def test_polls(self):
        self.run_django_manage_test('docs/tutorials/polls')

    def test_hello(self):
        self.run_django_manage_test('docs/tutorials/hello')

    def test_lets(self):
        self.run_django_manage_test('docs/tutorials/lets')

    def test_letsmti(self):
        self.run_django_manage_test('docs/tutorials/letsmti')

    def test_gfktest(self):
        self.run_django_manage_test('docs/tutorials/gfktest')

    def test_mldbc(self):
        self.run_django_manage_test('docs/tutorials/mldbc')

    def test_belref(self):
        self.run_django_manage_test("docs/tutorials/belref")

    def test_utils(self):
        self.run_simple_doctests('lino/utils/__init__.py')

    def test_float2decimal(self):
        if PYAFTER26:
            self.run_django_manage_test("docs/tested/float2decimal")

    def test_integer_pk(self):
        self.run_django_manage_test("docs/tested/integer_pk")



class CoreTests(TestCase):

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

    def test_01(self):
        self.run_simple_doctests("""
        lino/utils/instantiator.py
        lino/modlib/cal/utils.py
        """)

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

    def test_contacts_utils(self):
        self.run_simple_doctests('lino/modlib/contacts/utils.py')

    def test_addressable(self):
        self.run_simple_doctests('lino/utils/addressable.py')

    def test_cycler(self):
        self.run_simple_doctests('lino/utils/cycler.py')


class ProjectsTests(LinoTestCase):
    
    # def test_all(self):
    #     from atelier.fablib import run_in_demo_projects
    #     run_in_demo_projects('test')

    def test_events(self):
        self.run_django_manage_test("lino/projects/events")

    def test_belref(self):
        self.run_django_manage_test("lino/projects/belref")

    def test_babel_tutorial(self):
        self.run_django_manage_test("lino/projects/babel_tutorial")

    def test_min1(self):
        self.run_django_manage_test("lino/projects/min1")

    def test_min2(self):
        self.run_django_manage_test("lino/projects/min2")


class TestAppsTests(LinoTestCase):
    
    def test_20100212(self):
        self.run_django_admin_test_cd("lino/test_apps/20100212")

    def test_quantityfield(self):
        self.run_django_admin_test_cd("lino/test_apps/quantityfield")


class DumpTests(LinoTestCase):
    def test_dump2py(self):
        for prj in ["lino/projects/belref"]:
            p = Path(prj)
            tmp = p.child('tmp').absolute()
            tmp.rmtree()
            self.run_django_admin_command_cd(p, 'dump2py', tmp)
            self.assertEqual(tmp.child('restore.py').exists(), True)

from . import test_appy_pod
