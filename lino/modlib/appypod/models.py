# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils.appy_pod import PrintTableAction, PortraitPrintTableAction
from lino.core.tables import AbstractTable
AbstractTable.as_pdf = PrintTableAction()
AbstractTable.as_pdf_p = PortraitPrintTableAction()
