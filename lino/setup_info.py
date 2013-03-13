#~ """
#~ This is the current Lino version number.

#~ After editing this file, also edit the following files:

#~ - Release notes : ../docs/releases/<__version__>.rst
#~ - Releases overview: edit ../docs/releases/index.rst

#~ Related public URLs:

#~ - http://lino-framework.org/releases/
#~ - http://pypi.python.org/pypi/lino

#~ """
#~ __version__ = 


PACKAGES = [n for n in """
lino
lino.core
lino.history
lino.sandbox.bcss
lino.sandbox.contacts
lino.sandbox.contacts.fixtures
lino.sandbox.debts
lino.sandbox.debts.fixtures
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
lino.projects.crl
lino.projects.crl.fixtures
lino.projects.events
lino.projects.homeworkschool
lino.projects.homeworkschool.fixtures
lino.projects.igen
lino.projects.igen.tests
lino.projects.min1
lino.projects.min2
lino.projects.polls_tutorial
lino.projects.polls_tutorial.polls
lino.projects.polls_tutorial.polls.fixtures
lino.projects.presto
lino.projects.presto.fixtures
lino.projects.std
lino.projects.uiless.fixtures
lino.projects.uiless.mysite
lino.projects.uiless.polls
lino.projects.uiless.polls.fixtures
lino.projects.babel_tutorial
lino.projects.babel_tutorial.fixtures
""".splitlines() if n]
  
SETUP_INFO = dict(name = 'lino',
  version = '1.6.2',
  requires = ['North (==0.0.4)','appy',
    'python_dateutil','PyYAML','odfpy','jinja2',
    ],
  description = "A framework for writing desktop-like web applications using Django and ExtJS",
  long_description = """\
Lino is a high-level framework for writing desktop-like web applications
based on `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.

Lino is for IT professionals who want to develop customized database 
applications for their customers without writing any HTML or CSS.

Lino consists of different parts:

- `django-site <http://site.lino-framework.org>`__
  (split off from main project in March 2013)
  provides startup signals and the `settings.SITE` object.
  
- `django-north <https://code.google.com/p/django-north/>`__
  (split off from main project in March 2013)
  provides python dumps, babel fields and data migration.

- A collection of reusable Django apps and 
  out-of-the-box demo applications
- A collection of *user interface renderers*.
  Currently there's one for ExtJS 
  and another for Twitter/Bootstrap-based "plain" interface.

The following real-world applications use the Lino framework:

- `Lino-Welfare <http://welfare.lino-framework.org>`__
  
  """,
  license = 'GPL',
  packages = PACKAGES,
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://www.lino-framework.org",
  #~ test_suite = 'lino.test_apps',
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
