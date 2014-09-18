# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

if False:

    from lino.modlib.codechanges.models import change, issue

    change(20121222, "experimental", """
  Documenting code changes
  ------------------------
  The new module :mod:`lino.modlib.codechanges` is an attempt 
  to make it easier to write code change reports, 
  and to find them back when needed.
  :menuselection:`Explorer --> System --> Code Changes`
  currently displays a list of all changes.
  """)

    issue(20121222, "missing feature", """
  It seems that `detail_layout` doesn't work on `VirtualTable`.
  """)
