from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino','setup_info.py'),globals())

from djangosite.utils.pythontest import TestCase



class LinoTestCase(TestCase):
    demo_settings_module = "lino.projects.std.settings"
    #~ default_environ = dict(DJANGO_SETTINGS_MODULE="lino.projects.std.settings")
    project_root = ROOTDIR
    
class PackagesTests(LinoTestCase):
    def test_01(self): self.run_packages_test(SETUP_INFO['packages'])

class BlogTest(LinoTestCase):
    def test_20130316(self): self.run_simple_doctests('docs/blog/2013/0316.rst')
    def test_20130507(self): self.run_simple_doctests('docs/blog/2013/0507.rst')
    def test_20130508(self): self.run_simple_doctests('docs/blog/2013/0508.rst')
    #~ def test_20130513(self): self.run_simple_doctests('docs/blog/2013/0513.rst')
    #~ def test_20130622(self): self.run_simple_doctests('docs/blog/2013/0622.rst')
    #~ def test_20130714(self): self.run_simple_doctests('docs/blog/2013/0714.rst')
    def test_20130716(self): self.run_simple_doctests('docs/blog/2013/0716.rst')
    def test_20130719(self): self.run_simple_doctests('docs/blog/2013/0719.rst')
    #~ def test_20130807(self): self.run_simple_doctests('docs/blog/2013/0807.rst')
    #~ def test_20130821(self): self.run_simple_doctests('docs/blog/2013/0821.rst')
    
class DocsTests(LinoTestCase):

    def test_templates_api(self): self.run_simple_doctests('docs/user/templates_api.rst')
    #~ def test_actions(self): self.run_docs_django_tests('tutorials.actions.settings')
    def test_de_BE(self): self.run_docs_django_tests('tutorials.de_BE.settings')
    def test_auto_create(self): self.run_docs_django_tests('tutorials.auto_create.settings')
    def test_human(self): self.run_docs_django_tests('tutorials.human.settings')
    def test_pisa(self): self.run_docs_django_tests('tutorials.pisa.settings')
    
    def test_polls(self): self.run_django_manage_test('docs/tutorials/polls')
    def test_quickstart(self): self.run_django_manage_test('docs/tutorials/quickstart')
    def test_actions(self): self.run_django_manage_test('docs/tutorials/actions')
    def test_actors(self): self.run_django_manage_test('docs/tutorials/actors')


class UtilsTests(LinoTestCase):
    def test_01(self): self.run_simple_doctests('lino/utils/__init__.py')
    def test_02(self): self.run_simple_doctests('lino/utils/html2odf.py')
    def test_xmlgen_html(self): self.run_simple_doctests('lino/utils/xmlgen/html.py')
    def test_xmlgen_sepa(self): self.run_simple_doctests('lino/utils/xmlgen/sepa.py')
    def test_05(self): self.run_simple_doctests('lino/utils/memo.py')
    def test_06(self): self.run_simple_doctests('lino/utils/html2xhtml.py')
    def test_07(self): self.run_simple_doctests('lino/utils/demonames.py')
    def test_08(self): self.run_simple_doctests('lino/utils/odsreader.py')
    
    def test_ssin(self): self.run_simple_doctests('lino/utils/ssin.py')
    #~ def test_11(self): self.run_simple_doctests('lino/core/choicelists.py')
    def test_jsgen(self): self.run_simple_doctests('lino/utils/jsgen.py')
    def test_ranges(self): self.run_simple_doctests('lino/utils/ranges.py')

    def test_vat_utils(self): self.run_simple_doctests('lino/modlib/vat/utils.py')
    def test_ledger_utils(self): self.run_simple_doctests('lino/modlib/ledger/utils.py')
    def test_accounts_utils(self): self.run_simple_doctests('lino/modlib/accounts/utils.py')
    def test_contacts_utils(self): self.run_simple_doctests('lino/modlib/contacts/utils.py')
    def test_cal_utils(self): self.run_simple_doctests('lino/modlib/cal/utils.py')
    def test_mixins_addressable(self): self.run_simple_doctests('lino/mixins/addressable.py')

class I18nTests(LinoTestCase):
    def test_i18n(self): self.run_simple_doctests('docs/tested/test_i18n.rst')
    
class CosiTests(LinoTestCase):
    def test_cosi(self):      self.run_django_admin_test("lino.projects.cosi.settings") # covered by docs/tutorials/quickstart
    def test_cosi_demo(self): self.run_simple_doctests('docs/tested/test_cosi_demo.rst')
        
class ProjectsTests(LinoTestCase):
    
    def test_events(self): self.run_django_admin_test("lino.projects.events.settings") 
    def test_presto(self): self.run_django_admin_test("lino.projects.presto.test_settings") 
    def test_belref(self): self.run_django_admin_test("lino.projects.belref.settings") 
    def test_babel_tutorial(self): self.run_django_admin_test("lino.projects.babel_tutorial.settings") 
    def test_homeworkschool(self): self.run_django_admin_test("lino.projects.homeworkschool.settings.demo") 
    def test_min1(self): self.run_django_admin_test("lino.projects.min1.settings") 
    def test_min2(self): self.run_django_admin_test("lino.projects.min2.settings") 
    
class Tutorials(LinoTestCase):
    def test_lets(self): self.run_django_admin_test("lino.tutorials.lets1.settings") 
    def test_mini(self): self.run_django_admin_test("lino.tutorials.mini.settings") 
    
class TestAppsTests(LinoTestCase):
    
    #~ def test_nomti(self): self.run_django_admin_test("lino.test_apps.nomti.settings") 
    #~ NotImplementedError: No LayoutElement for owners (<class 'django.db.models.fields.related.ManyToManyField'>) in ListLayout on nomti.PlaceTable
    
    def test_20100212(self): self.run_django_admin_test("lino.test_apps.20100212.settings") 
    def test_quantityfield(self): self.run_django_admin_test("lino.test_apps.quantityfield.settings") 
    


#~ class PrestoTest(LinoTestCase):
    #~ demo_settings_module = "lino.projects.presto.test_settings"
    
    #~ def test_presto_demo(self): self.run_docs_django_tests('lino.projects.presto.settings')
    #~ def test_presto_demo(self): self.run_django_admin_test('lino.projects.presto.settings')
