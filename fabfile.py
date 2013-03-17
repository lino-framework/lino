from djangosite.utils.fablib import *
setup_from_project('lino')  

env.tolerate_sphinx_warnings = True

# invoke only these with ``fab t3``:
env.django_doctests.append('tutorials.de_BE.settings')
env.django_doctests.append('tutorials.auto_create.settings')
env.django_doctests.append('tutorials.human.settings')

# invoke only these with ``fab t4``:
env.simple_doctests.append('lino/utils/html2odf.py')
env.simple_doctests.append('docs/blog/2013/0316.rst')
env.simple_doctests.append('lino/utils/xmlgen/html.py')
env.simple_doctests.append('lino/utils/memo.py')
env.simple_doctests.append('lino/modlib/contacts/utils.py')
env.simple_doctests.append('lino/utils/html2xhtml.py')
env.simple_doctests.append('lino/utils/demonames.py')
env.simple_doctests.append('lino/utils/odsreader.py')
env.simple_doctests.append('lino/utils/ssin.py')
env.simple_doctests.append('lino/core/choicelists.py')
env.simple_doctests.append('lino/utils/jsgen.py')
env.simple_doctests.append('lino/utils/ranges.py')
env.simple_doctests.append('lino/modlib/ledger/utils.py')
env.simple_doctests.append('lino/modlib/accounts/utils.py')
  
env.django_admin_tests += [
      "lino.projects.cosi.settings",
      "lino.projects.events.settings",
      "lino.test_apps.nomti.settings",
      "lino.test_apps.20100212.settings",
      "lino.test_apps.quantityfield.settings",
      #~ "lino.test_apps.human.settings",
      "lino.projects.cosi.settings",
      #~ "lino.projects.presto.settings", 
      "lino.projects.babel_tutorial.settings",
      "lino.projects.polls_tutorial.settings",
      "lino.projects.belref.settings",
      "lino.projects.events.settings",
      "lino.projects.homeworkschool.settings",
      "lino.projects.min1.settings",
      "lino.projects.min2.settings",
]


