from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino','setup_info.py'),globals())

from djangosite.utils.pythontest import TestCase



class LinoTestCase(TestCase):
    demo_settings_module = "lino.projects.std.settings"
    #~ default_environ = dict(DJANGO_SETTINGS_MODULE="lino.projects.std.settings")
    project_root = ROOTDIR
    
class BlogTest(LinoTestCase):
    def test_20130316(self): self.run_simple_doctests('docs/blog/2013/0316.rst')
    def test_20130507(self): self.run_simple_doctests('docs/blog/2013/0507.rst')
    def test_20130508(self): self.run_simple_doctests('docs/blog/2013/0508.rst')
    #~ def test_20130513(self): self.run_simple_doctests('docs/blog/2013/0513.rst')
    
class DocsTests(LinoTestCase):

    def test_01(self): self.run_docs_django_tests('tutorials.de_BE.settings')
    def test_02(self): self.run_docs_django_tests('tutorials.auto_create.settings')
    def test_03(self): self.run_docs_django_tests('tutorials.human.settings')
    
    def test_polls(self): self.run_django_manage_test('docs/tutorials/polls')
    def test_quickstart(self): self.run_django_manage_test('docs/tutorials/quickstart')


class UtilsTests(LinoTestCase):
    def test_01(self): self.run_simple_doctests('lino/utils/__init__.py')
    def test_02(self): self.run_simple_doctests('lino/utils/html2odf.py')
    def test_04(self): self.run_simple_doctests('lino/utils/xmlgen/html.py')
    def test_05(self): self.run_simple_doctests('lino/utils/memo.py')
    def test_06(self): self.run_simple_doctests('lino/utils/html2xhtml.py')
    def test_07(self): self.run_simple_doctests('lino/utils/demonames.py')
    def test_08(self): self.run_simple_doctests('lino/utils/odsreader.py')
    
    def test_10(self): self.run_simple_doctests('lino/utils/ssin.py')
    #~ def test_11(self): self.run_simple_doctests('lino/core/choicelists.py')
    def test_12(self): self.run_simple_doctests('lino/utils/jsgen.py')
    def test_13(self): self.run_simple_doctests('lino/utils/ranges.py')

    def test_24(self): self.run_simple_doctests('lino/modlib/ledger/utils.py')
    def test_25(self): self.run_simple_doctests('lino/modlib/accounts/utils.py')
    def test_26(self): self.run_simple_doctests('lino/modlib/contacts/utils.py')

class PackagesTests(LinoTestCase):
    """
    Runs certain tests related to packaging.
    """
    def test_01(self): self.run_packages_test(SETUP_INFO['packages'])

class CosiTests(LinoTestCase):
    def test_cosi(self):      self.run_django_admin_test("lino.projects.cosi.settings") # covered by docs/tutorials/quickstart
    def test_cosi_demo(self): self.run_simple_doctests('docs/tested/test_cosi_demo.rst')
        
class ProjectsTests(LinoTestCase):
    
    def test_events(self): self.run_django_admin_test("lino.projects.events.settings") 
    def test_presto(self): self.run_django_admin_test("lino.projects.presto.test_settings") 
    def test_belref(self): self.run_django_admin_test("lino.projects.belref.settings") 
    def test_babel_tutorial(self): self.run_django_admin_test("lino.projects.babel_tutorial.settings") 
    def test_homeworkschool(self): self.run_django_admin_test("lino.projects.homeworkschool.settings") 
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
