.. _noi.tested.clocking:

Clocking
========

The :mod:`lino.modlib.clocking` module is for doing time tracking.

.. include:: /include/tested.rst

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.api.doctest import *

>>> ses = rt.login("robin")

>>> ses.show(clocking.Sessions)
... #doctest: +REPORT_UDIFF
================================ ============ ============ ============ ========== ========== ============ ========= ==========
 Ticket                           Author       Start date   Start time   End Date   End Time   Break Time   Summary   Duration
-------------------------------- ------------ ------------ ------------ ---------- ---------- ------------ --------- ----------
 #5 (Cannot create Foo)           Robin Rood   5/23/15      13:12:00     5/23/15    13:18:00                          0:06
 #4 (Foo and bar don't baz)       jean         5/23/15      13:09:00     5/23/15    13:12:00                          0:03
 #3 (Baz sucks)                   luc          5/23/15      12:49:00     5/23/15    13:09:00                          0:20
 #2 (Bar is not always baz)       marc         5/23/15      12:29:00     5/23/15    12:49:00                          0:20
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      12:19:00     5/23/15    12:29:00                          0:10
 #5 (Cannot create Foo)           Robin Rood   5/23/15      11:59:00     5/23/15    12:19:00                          0:20
 #4 (Foo and bar don't baz)       jean         5/23/15      11:46:00     5/23/15    11:59:00                          0:13
 #3 (Baz sucks)                   luc          5/23/15      11:34:00     5/23/15    11:46:00                          0:12
 #2 (Bar is not always baz)       marc         5/23/15      11:29:00     5/23/15    11:34:00                          0:05
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      11:06:00     5/23/15    11:29:00                          0:23
 #5 (Cannot create Foo)           Robin Rood   5/23/15      10:49:00     5/23/15    11:06:00                          0:17
 #4 (Foo and bar don't baz)       jean         5/23/15      10:43:00     5/23/15    10:49:00                          0:06
 #3 (Baz sucks)                   luc          5/23/15      10:40:00     5/23/15    10:43:00                          0:03
 #2 (Bar is not always baz)       marc         5/23/15      10:20:00     5/23/15    10:40:00                          0:20
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      10:00:00     5/23/15    10:20:00                          0:20
 #5 (Cannot create Foo)           Robin Rood   5/23/15      09:50:00     5/23/15    10:00:00                          0:10
 #4 (Foo and bar don't baz)       jean         5/23/15      09:30:00     5/23/15    09:50:00                          0:20
 #3 (Baz sucks)                   luc          5/23/15      09:17:00     5/23/15    09:30:00                          0:13
 #2 (Bar is not always baz)       marc         5/23/15      09:05:00     5/23/15    09:17:00                          0:12
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      09:00:00     5/23/15    09:05:00                          0:05
 **Total (20 rows)**                                                                                                  **4:18**
================================ ============ ============ ============ ========== ========== ============ ========= ==========
<BLANKLINE>
