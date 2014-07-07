.. _noi.tested.smtpd:

SMTP server
===========

Lino Noi has a recmail command which starts an SMTP server.

.. include:: /include/tested.rst

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> ses = dd.login("robin")

>>> print(settings.SITE.welcome_text())  #doctest: +ELLIPSIS
This is Lino Noi using ...


