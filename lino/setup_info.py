# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

SETUP_INFO = dict(
    name='lino',
    version='1.6.15',  # not yet released
    install_requires=[
        'django<1.7', 'Sphinx',
        'atelier', 'unipath', 'python_dateutil',
        'Babel', 'odfpy',
        'jinja2', 'appy', 'pytidylib', 'PyYAML',
        'django-iban', 'xlwt', 'xlrd'],
    tests_require=[
        'beautifulsoup4', 'html5lib', 'reportlab==2.7', 'pisa'],
    # pisa has a bug which makes it complain that "Reportlab Version
    # 2.1+ is needed!" when reportlab 3 is installed.
    # So we install reportlab 2.7 (the latest 2.x version)

    description="A framework for writing desktop-like web applications "
    "using Django and ExtJS",
    license='BSD License',
    include_package_data=True,
    zip_safe=False,
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://www.lino-framework.org",
    #~ test_suite = 'lino.test_apps',
    test_suite='tests',
    classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: BSD License
  Natural Language :: English
  Natural Language :: French
  Natural Language :: German
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Home Automation
  Topic :: Office/Business
  Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())

SETUP_INFO.update(long_description="""\
Lino is a high-level framework for writing desktop-like customized
database applications based on `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.
Lino applications are Django projects
where the application developer does not need to write any
URLconf, HTML nor CSS (`more <http://lino-framework.org/about/what.html>`__).

Examples of Lino applications are
`Lino Welfare <http://welfare.lino-framework.org>`__,
`Lino Così <http://cosi.lino-framework.org>`__
or
`Lino Faggio <http://faggio.lino-framework.org>`__
(`more <http://lino-framework.org/about/projects.html>`__)

""")

SETUP_INFO.update(packages=[str(n) for n in """
lino
lino.core
lino.history
lino.management
lino.management.commands
lino.mixins
lino.modlib
lino.modlib.auto
lino.modlib.auto.sales
lino.modlib.addresses
lino.modlib.appypod
lino.modlib.awesomeuploader
lino.modlib.beid
lino.modlib.boards
lino.modlib.bootstrap3
lino.modlib.cal
lino.modlib.cal.fixtures
lino.modlib.cal.management
lino.modlib.cal.management.commands
lino.modlib.cal.workflows
lino.modlib.cv
lino.modlib.cv.fixtures
lino.modlib.contacts
lino.modlib.contacts.fixtures
lino.modlib.contacts.management
lino.modlib.contacts.management.commands
lino.modlib.contenttypes
lino.modlib.contenttypes.fixtures
lino.modlib.countries
lino.modlib.countries.fixtures
lino.modlib.davlink
lino.modlib.dedupe
lino.modlib.excerpts
lino.modlib.export_excel
lino.modlib.extensible
lino.modlib.extjs
lino.modlib.eid_jslib
lino.modlib.eid_jslib.beid
lino.modlib.families
lino.modlib.finan
lino.modlib.finan.fixtures
lino.modlib.humanlinks
lino.modlib.humanlinks.fixtures
lino.modlib.iban
lino.modlib.importfilters
lino.modlib.languages
lino.modlib.languages.fixtures
lino.modlib.ledger
lino.modlib.ledger.fixtures
lino.modlib.lists
lino.modlib.lists.fixtures
lino.modlib.notes
lino.modlib.notes.fixtures
lino.modlib.print_pisa
lino.modlib.products
lino.modlib.products.fixtures
lino.modlib.projects
lino.modlib.properties
lino.modlib.rooms
lino.modlib.sales
lino.modlib.sales.fixtures
lino.modlib.uploads
lino.modlib.users
lino.modlib.users.fixtures
lino.modlib.thirds
lino.modlib.reception
lino.modlib.tickets
lino.modlib.tickets.fixtures
lino.modlib.vocbook
lino.modlib.outbox
lino.modlib.outbox.fixtures
lino.modlib.blogs
lino.modlib.workflows
lino.modlib.polls
lino.modlib.polls.fixtures
lino.modlib.postings
lino.modlib.accounts
lino.modlib.vat
lino.modlib.households
lino.modlib.households.fixtures
lino.modlib.courses
lino.modlib.about
lino.modlib.pages
lino.modlib.pages.fixtures
lino.modlib.codechanges
lino.modlib.orders
lino.modlib.changes
lino.modlib.comments
lino.modlib.concepts
lino.modlib.declarations
lino.modlib.events
lino.modlib.events.fixtures
lino.modlib.events.tests
lino.modlib.smtpd
lino.modlib.smtpd.management
lino.modlib.smtpd.management.commands
lino.modlib.statbel
lino.modlib.statbel.fixtures
lino.modlib.sepa
lino.modlib.sepa.fixtures
lino.modlib.system
lino.modlib.system.fixtures
lino.modlib.system.tests
lino.projects
lino.projects.belref
lino.projects.belref.fixtures
lino.projects.belref.settings
lino.projects.cms
lino.projects.cms.fixtures
lino.projects.crl
lino.projects.crl.fixtures
lino.projects.estref
lino.projects.estref.settings
lino.projects.events
lino.projects.homeworkschool
lino.projects.homeworkschool.settings
lino.projects.homeworkschool.fixtures
lino.projects.i18n
lino.projects.igen
lino.projects.igen.tests
lino.projects.min1
lino.projects.min1.settings
lino.projects.min2
lino.projects.min2.settings
lino.projects.min2.modlib
lino.projects.min2.modlib.contacts
lino.projects.min2.modlib.contacts.fixtures
lino.projects.min2.tests
lino.projects.polly
lino.projects.polly.settings
lino.projects.presto
lino.projects.presto.fixtures
lino.projects.presto.settings
lino.projects.presto.modlib
lino.projects.presto.modlib.contacts
lino.projects.presto.modlib.contacts.fixtures
lino.projects.presto.tests
lino.projects.std
lino.projects.babel_tutorial
lino.projects.babel_tutorial.fixtures
lino.projects.docs
lino.projects.docs.settings
lino.sphinxcontrib
lino.sphinxcontrib.logo
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
lino.tests
lino.tutorials
lino.tutorials.mini
lino.tutorials.lets1
lino.tutorials.lets1.fixtures
lino.tutorials.lets1.lets
lino.ui
lino.utils
lino.utils.demonames
lino.utils.mldbc
lino.utils.xmlgen
lino.utils.xmlgen.intervat
lino.utils.xmlgen.cbss
lino.utils.xmlgen.odf
lino.utils.xmlgen.sepa
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino': [
        ('**/sandbox/**',        'ignore', None),
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**/linoweb.js',        'jinja2', None),
        #~ ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
        #~ ('**/templates/**.txt',  'genshi', {
        #~ 'template_class': 'genshi.template:TextTemplate'
        #~ })
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    package = str(package)
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

add_package_data('lino', 'config/*.odt')
add_package_data('lino.modlib.cal', 'config/*.odt')
add_package_data('lino.modlib.notes', 'config/notes/Note/*.odt')
add_package_data('lino.modlib.outbox', 'config/outbox/Mail/*.odt')
add_package_data('lino.modlib.languages.fixtures', '*.tab')

l = add_package_data('lino')
for lng in 'de fr et nl'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
