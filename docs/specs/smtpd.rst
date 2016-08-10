.. _noi.tested.smtpd:

SMTP server
===========

.. how to test only this document:
   $ python setup.py test -s tests.DocsTests.test_clocking

Lino Noi has a recmail command which starts an SMTP server.

.. include:: /include/tested.rst

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.api.shell import *
>>> from django.test.client import Client
>>> ses = rt.login("robin")

>>> print(settings.SITE.welcome_text())  #doctest: +ELLIPSIS
This is Lino Noi ... using ...

