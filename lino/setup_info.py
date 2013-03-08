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

SETUP_INFO=dict(name = 'lino',
  version = '1.6.0',
  description = "A framework for writing desktop-like web applications using Django and ExtJS",
  long_description = """\
Lino is a framework for writing desktop-like web applications 
using `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.

Lino is for Python developers who want to develop 
Lino applications for their customers.
Primary target customers for Lino applications 
are agencies and companies who need a 
*customized database application*.

Lino the framework consists of different parts:

- `django-site <http://site.lino-framework.org>`__
  (split off from main project in March 2013)
  provides startup signals and the `settings.SITE` object
  
- `django-north <https://code.google.com/p/django-north/>`__
  (split off from main project in March 2013)
  provides python dumps, babel fields and data migration.

- :mod:`lino.modlib`, a collection of reusable Django apps
- A collection of out-of-the-box demo applications
- The default "plain" user interface 
- The optional ExtJS user interface 

The following real-world applications use the Lino framework:

- `Lino-Welfare <http://welfare.lino-framework.org>`__
  
  """,
  license = 'GPL',
  packages = ['lino'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['Django','appy','python_dateutil','PyYAML','odfpy','sphinx','jinja2'],
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
