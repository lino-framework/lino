# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Database models for `lino.modlib.appypod`.

.. autosummary::

"""


from lino.utils.appy_pod import PrintTableAction, PortraitPrintTableAction
from lino.core.tables import AbstractTable
AbstractTable.as_pdf = PrintTableAction()
AbstractTable.as_pdf_p = PortraitPrintTableAction()
