.. _noi.tested.smtpd:

SMTP server
===========

Lino Noi has a recmail command which starts an SMTP server.

.. include:: /include/tested.rst

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.api.shell import *
>>> from django.test.client import Client
>>> ses = rt.login("robin")

>>> print(settings.SITE.welcome_text())  #doctest: +ELLIPSIS
This is Lino Noi 0.0.1 using ...


>>> ses.show(clocking.Sessions)
... #doctest: +REPORT_UDIFF
===================== ============ ============ ============ ========== ========== ============ ========= ==========
 Ticket                Author       Start date   Start time   End Date   End Time   Break Time   Summary   Duration
--------------------- ------------ ------------ ------------ ---------- ---------- ------------ --------- ----------
 #2 (Bar)              Robin Rood   5/22/15      13:12:00     5/22/15    13:18:00                          0:06
 #1 (Foo)              Robin Rood   5/22/15      13:09:00     5/22/15    13:12:00                          0:03
 #3 (Baz)              Robin Rood   5/22/15      12:49:00     5/22/15    13:09:00                          0:20
 #2 (Bar)              Robin Rood   5/22/15      12:29:00     5/22/15    12:49:00                          0:20
 #1 (Foo)              Robin Rood   5/22/15      12:19:00     5/22/15    12:29:00                          0:10
 #3 (Baz)              Robin Rood   5/22/15      11:59:00     5/22/15    12:19:00                          0:20
 #2 (Bar)              Robin Rood   5/22/15      11:46:00     5/22/15    11:59:00                          0:13
 #1 (Foo)              Robin Rood   5/22/15      11:34:00     5/22/15    11:46:00                          0:12
 #3 (Baz)              Robin Rood   5/22/15      11:29:00     5/22/15    11:34:00                          0:05
 #2 (Bar)              Robin Rood   5/22/15      11:06:00     5/22/15    11:29:00                          0:23
 #1 (Foo)              Robin Rood   5/22/15      10:49:00     5/22/15    11:06:00                          0:17
 #3 (Baz)              Robin Rood   5/22/15      10:43:00     5/22/15    10:49:00                          0:06
 #2 (Bar)              Robin Rood   5/22/15      10:40:00     5/22/15    10:43:00                          0:03
 #1 (Foo)              Robin Rood   5/22/15      10:20:00     5/22/15    10:40:00                          0:20
 #3 (Baz)              Robin Rood   5/22/15      10:00:00     5/22/15    10:20:00                          0:20
 #2 (Bar)              Robin Rood   5/22/15      09:50:00     5/22/15    10:00:00                          0:10
 #1 (Foo)              Robin Rood   5/22/15      09:30:00     5/22/15    09:50:00                          0:20
 #3 (Baz)              Robin Rood   5/22/15      09:17:00     5/22/15    09:30:00                          0:13
 #2 (Bar)              Robin Rood   5/22/15      09:05:00     5/22/15    09:17:00                          0:12
 #1 (Foo)              Robin Rood   5/22/15      09:00:00     5/22/15    09:05:00                          0:05
 **Total (20 rows)**                                                                                       **4:18**
===================== ============ ============ ============ ========== ========== ============ ========= ==========
<BLANKLINE>
