# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

SETUP_INFO = dict(
    name='lino-noi',
    version='0.0.2',  # since 20150918
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
    license='GNU Affero General Public License v3',
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
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_noi',
    'lino_noi.lib',
    'lino_noi.lib.noi',
    'lino_noi.lib.noi.fixtures',
    'lino_noi.lib.contacts',
    'lino_noi.lib.products',
    'lino_noi.lib.users',
    'lino_noi.lib.users.fixtures',
    'lino_noi.projects.bs3',
    'lino_noi.projects.bs3.settings',
    'lino_noi.projects.bs3.tests',
    'lino_noi.projects',
    'lino_noi.projects.team',
    'lino_noi.projects.team.tests',
    'lino_noi.projects.team.settings',
    'lino_noi.projects.public',
    'lino_noi.projects.public.settings',
    'lino_noi.projects.public.tests',
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
