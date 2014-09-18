# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This fixture defines the content for pages `/man` and below.
Another attempt to provide a user manual.

This is a "reloadable" fixture. If you say::

  python manage.py loaddata man
  
it will overwrite existing web pages.

"""

from __future__ import unicode_literals

from django.conf import settings

from lino.modlib.pages.builder import page, objects

page('man', 'en', 'User manual', """
This is the user manual for 
`{{site.verbose_name}} <{{site.url}}>`__
version {{site.version}}.
""")

page('man', 'de', 'Benutzerhandbuch', """
Benutzerhandbuch für 
`{{site.verbose_name}} <{{site.url}}>`__
version {{site.version}}.
""")

page('models', 'en', 'Model reference', """
These are the models used in {{site.verbose_name}}.

{{as_table('about.Models')}}

""", parent='man')
