# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Josef Kejzlar, Luc Saffre, Hamza Khchine
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.export_excel`.

"""
from builtins import str
from builtins import zip
from builtins import object
import os

from django.conf import settings
from lino.core import actions
from lino.core.tables import AbstractTable
from lino.utils.media import TmpMediaFile
from django.utils.translation import ugettext_lazy as _


class TableRenderer(object):
    def __init__(self, ar):
        self.ar = ar

        # Internal iterator
        self.column = None
        self.row = None

    def get_columns(self):
        return self.ar.get_field_info()

    def get_rows(self):
        return self.ar.data_iterator

    @property
    def title(self):
        return self.ar.get_title()

    @property
    def columns(self):
        for column in zip(*self.get_columns()):
            self.column = column
            yield self.column

    @property
    def rows(self):
        for row in self.get_rows():
            self.row = row
            yield row

    @property
    def value(self):
        return self.column[0].field._lino_atomizer.full_value_from_object(
            self.row, self.ar)

    @property
    def value_as_text(self):
        return self.column[0].format_value(self.ar, self.value)

    @property
    def value_as_html(self):
        return self.column[0].value2html(self.ar, self.value)

    @property
    def column_name(self):
        return self.column[1]

    @property
    def column_width(self):
        return self.column[2]


def sheet_name(s):
    s = s[:31]
    for c in u"[]:\\?/*\x00":
        s = s.replace(c, '_')
    return s


class ExcelRenderer(TableRenderer):
    def render(self):
        # local import to avoid the following traceback:
        # Error in sys.exitfunc:
        # Traceback (most recent call last):
        #   File "/usr/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
        #     func(*targs, **kargs)
        #   File "/openpyxl/writer/write_only.py", line 38, in _openpyxl_shutdown
        #     for path in ALL_TEMP_FILES:
        # TypeError: 'NoneType' object is not iterable

        from openpyxl import Workbook
        from openpyxl.styles import Font

        workbook = Workbook(guess_types=True)
        sheet = workbook.active
        sheet.title = sheet_name(self.title)

        bold_font = Font(name='Calibri', size=11, bold=True, )
        for c, column in enumerate(self.columns):
            sheet.cell(row=1, column=c + 1).value = str(self.column_name)
            sheet.cell(row=1, column=c + 1).font = bold_font
            # sheet.col(c).width = min(256 * self.column_width / 7, 65535)
            # 256 == 1 character width, max width=65535

        for c, column in enumerate(self.columns):
            for r, row in enumerate(self.rows, start=1):
                try:
                    if type(self.value) == bool:
                        sheet.cell(row=r + 1, column=c + 1).value = self.value and 1 or 0
                    else:
                        sheet.cell(row=r + 1, column=c + 1).value = self.value
                except Exception:
                    sheet.cell(row=r + 1, column=c + 1).value = self.value_as_text

        return workbook


class ExportExcelAction(actions.Action):
    label = _("Export to .xls")
    help_text = _('Export this table as an .xls document')
    icon_name = 'page_excel'
    sort_index = -5
    select_rows = False
    default_format = 'ajax'
    preprocessor = "Lino.get_current_grid_config"

    def is_callable_from(self, caller):
        return isinstance(caller, actions.GridEdit)

    def run_from_ui(self, ar, **kw):
        # Prepare tmp file
        mf = TmpMediaFile(ar, 'xlsx')
        settings.SITE.makedirs_if_missing(os.path.dirname(mf.name))

        # Render
        self.render(ar, mf.name)

        # Tell client that the action was successful and that it
        # should open a new browser window on the generated file.
        ar.success(open_url=mf.url)

    def render(self, ar, file):
        workbook = ExcelRenderer(ar).render()
        workbook.save(file)


AbstractTable.export_excel = ExportExcelAction()
