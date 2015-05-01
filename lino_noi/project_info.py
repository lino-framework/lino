# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-noi',
    version='0.0.1',
    install_requires=['lino', 'xlwt'],
    test_suite='tests',
    description="A Lino application for managing local communities",
    long_description="""\
Lino Noi is a `Lino <http://www.lino-framework.org>`_ application
for managing teams who use a ticketing system.  The name comes from
Italian "noi" which means "we".

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://noi.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_noi',
    'lino_noi.fixtures',
    'lino_noi.lib',
    'lino_noi.lib.main',
    'lino_noi.lib.contacts',
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
