# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Josef Kejzlar, Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` for `lino.modlib.export_excel`.

"""
import os
import datetime

from django.conf import settings
from lino.core import actions
from lino.core.tables import AbstractTable
from lino.utils.media import TmpMediaFile
from django.utils.translation import ugettext_lazy as _
import xlwt


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
        return self.column[0].field._lino_atomizer.full_value_from_object(self.row, self.ar)

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
        s = s.replace('/', '_')
    return s


class ExcelRenderer(TableRenderer):
    default_style = xlwt.XFStyle()

    date_style = xlwt.XFStyle()
    date_style.num_format_str = 'yyyy-mm-dd'

    datetime_style = xlwt.XFStyle()
    datetime_style.num_format_str = 'yyyy-mm-dd h:mm:ss'

    time_style = xlwt.XFStyle()
    time_style.num_format_str = 'h:mm:ss'

    def render(self):
        workbook = xlwt.Workbook(encoding='utf-8')

        sheet = workbook.add_sheet(sheet_name(self.title))

        header_style = xlwt.easyxf("font: bold on;")
        for c, column in enumerate(self.columns):
            sheet.write(0, c, self.column_name, header_style)
            sheet.col(c).width = min(256 * self.column_width / 7, 65535)
            # 256 == 1 character width, max width=65535

        for c, column in enumerate(self.columns):
            for r, row in enumerate(self.rows, start=1):
                try:
                    value = self.value
                    style = self.default_style

                    if isinstance(value, datetime.date):
                        style = self.date_style

                    if isinstance(value, datetime.datetime):
                        style = self.datetime_style

                    if isinstance(value, datetime.time):
                        style = self.time_style

                    sheet.write(r, c, value, style=style)
                except Exception:
                    sheet.write(r, c, self.value_as_text)

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
        mf = TmpMediaFile(ar, 'xls')
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
