SETUP_INFO = dict(name = 'lino',
  version = '1.6.10',
  install_requires = ['North==0.1.5','djangosite>=0.1.5','PyYAML','odfpy','jinja2','appy'],
  description = "A framework for writing desktop-like web applications using Django and ExtJS",
  license = 'GPL',
  include_package_data = True,
  zip_safe = False,
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://www.lino-framework.org",
  #~ test_suite = 'lino.test_apps',
  test_suite = 'tests',
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: GNU General Public License (GPL)
  Natural Language :: English
  Natural Language :: French
  Natural Language :: German
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Home Automation
  Topic :: Office/Business
  Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())

SETUP_INFO.update(long_description = """\
Lino is a high-level framework for writing desktop-like customized 
database applications based on `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.
A Lino application is technically just a Django project, 
but the application developer does not need to write any 
URLconf, HTML nor CSS (`more <http://lino-framework.org/about>`_)

The following real-world applications use the Lino framework:

- `Lino-Welfare <http://welfare.lino-framework.org>`__

Lino uses the following projects by the same author:

- `atelier <http://atelier.lino-framework.org>`__
  provides some general Python tools.
  
- `djangosite <http://site.lino-framework.org>`__
  provides startup signals and the `settings.SITE` object.
  
- `north <http://north.lino-framework.org>`__
  provides python dumps, multilingual database content 
  and data migration.

  
""")

SETUP_INFO.update(packages = [str(n) for n in """
lino
lino.core
lino.extjs
lino.history
lino.modlib
lino.modlib.contacts
lino.modlib.contacts.fixtures
lino.modlib.countries
lino.modlib.countries.fixtures
lino.modlib.finan
lino.modlib.finan.fixtures
lino.modlib.ledger
lino.modlib.ledger.fixtures
lino.modlib.links
lino.modlib.links.fixtures
lino.modlib.links.tests
lino.modlib.notes
lino.modlib.notes.fixtures
lino.modlib.products
lino.modlib.products.fixtures
lino.modlib.projects
lino.modlib.sales
lino.modlib.sales.fixtures
lino.modlib.uploads
lino.modlib.properties
lino.modlib.users
lino.modlib.thirds
lino.modlib.cal
lino.modlib.cal.management
lino.modlib.cal.management.commands
lino.modlib.cal.fixtures
lino.modlib.cal.tests
lino.modlib.cal.workflows
lino.modlib.tickets
lino.modlib.tickets.fixtures
lino.modlib.vocbook
lino.modlib.outbox
lino.modlib.outbox.fixtures
lino.modlib.blogs
lino.modlib.workflows
lino.modlib.postings
lino.modlib.accounts
lino.modlib.vat
lino.modlib.households
lino.modlib.households.fixtures
lino.modlib.school
lino.modlib.school.fixtures
lino.modlib.about
lino.modlib.pages
lino.modlib.pages.fixtures
lino.modlib.codechanges
lino.modlib.orders
lino.modlib.changes
lino.modlib.concepts
lino.modlib.partners
lino.modlib.partners.fixtures
lino.modlib.declarations
lino.modlib.events
lino.modlib.events.fixtures
lino.modlib.events.tests
lino.test_apps
lino.test_apps.20090714
lino.test_apps.20090717
lino.test_apps.20100126
lino.test_apps.20100127
lino.test_apps.20100206
lino.test_apps.20100212
lino.test_apps.chooser
lino.test_apps.properties
lino.test_apps.example
lino.test_apps.quantityfield
lino.test_apps.20121124
lino.test_apps.mti
lino.test_apps.nomti
lino.utils
lino.utils.xmlgen
lino.utils.xmlgen.intervat
lino.utils.xmlgen.cbss
lino.utils.xmlgen.odf
lino.tutorials
lino.tutorials.mini
lino.tutorials.lets1
lino.tutorials.lets1.fixtures
lino.tutorials.lets1.lets
lino.management
lino.management.commands
lino.mixins
lino.ui
lino.ui.fixtures
lino.ui.tests
lino.projects
lino.projects.belref
lino.projects.belref.fixtures
lino.projects.cms
lino.projects.cms.fixtures
lino.projects.cosi
lino.projects.cosi.fixtures
lino.projects.cosi.tests
lino.projects.cosi.settings
lino.projects.crl
lino.projects.crl.fixtures
lino.projects.events
lino.projects.homeworkschool
lino.projects.homeworkschool.fixtures
lino.projects.igen
lino.projects.igen.tests
lino.projects.min1
lino.projects.min2
lino.projects.unused_polls_tutorial
lino.projects.unused_polls_tutorial.polls
lino.projects.unused_polls_tutorial.polls.fixtures
lino.projects.presto
lino.projects.presto.fixtures
lino.projects.std
lino.projects.babel_tutorial
lino.projects.babel_tutorial.fixtures
""".splitlines() if n])
  
SETUP_INFO.update(message_extractors = {
    'lino': [
        ('**/sandbox/**',        'ignore', None),
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**/linoweb.js',        'jinja2', None),
        #~ ('**.js',                'javascript', None),
        ('**/templates_jinja/**.html', 'jinja2', None),
        #~ ('**/templates/**.txt',  'genshi', {
            #~ 'template_class': 'genshi.template:TextTemplate'
        #~ })
    ],
})

SETUP_INFO.update(package_data=dict())
def add_package_data(package,*patterns):
    l = SETUP_INFO['package_data'].setdefault(package,[])
    l.extend(patterns)
    return l

add_package_data('lino','config/*.odt')
add_package_data('lino.modlib.cal','config/*.odt')
add_package_data('lino.modlib.notes','config/notes/Note/*.odt')
add_package_data('lino.modlib.outbox','config/outbox/Mail/*.odt')

l = add_package_data('lino')
for lng in 'de fr et nl'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
