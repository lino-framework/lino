# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-noi',
    version='0.0.1',
    install_requires=['lino', 'xlwt'],
    test_suite='tests',
    description="The Lino application used by the Lino team for managing their work on the Lino project",
    long_description="""\
Lino Noi is the `Lino <http://www.lino-framework.org>`_
application used by the Lino team for managing their work on the Lino project.
The name comes from Italian "noi" which means "we".

It can be called a `DevOps tool
<https://en.wikipedia.org/wiki/DevOps>`_ in that it stresses
communication, collaboration, integration, automation, and measurement
of cooperation between software developers, users and other IT
professionals.

""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://noi.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Office/Business :: Scheduling
Topic :: Office/Business :: Groupware
Topic :: Software Development :: Bug Tracking
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_noi',
    'lino_noi.fixtures',
    'lino_noi.lib',
    'lino_noi.lib.noi',
    'lino_noi.lib.contacts',
    'lino_noi.lib.products',
    'lino_noi.lib.users',
    'lino_noi.lib.users.fixtures',
    'lino_noi.settings',
])

SETUP_INFO.update(message_extractors={
    'lino_noi': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

l = add_package_data('lino_noi')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
