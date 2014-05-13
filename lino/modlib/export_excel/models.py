import os
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
    def value_as_html(self):
        return self.column[0].value2html(self.ar, self.value)

    @property
    def column_name(self):
        return self.column[1]

    @property
    def column_width(self):
        return self.column[2]


class ExcelRenderer(TableRenderer):
    def render(self):
        workbook = xlwt.Workbook(encoding='utf-8', style_compression=1)

        sheet = workbook.add_sheet(self.title)

        header_style = xlwt.easyxf("font: bold on;")
        for c, column in enumerate(self.columns):
            sheet.write(0, c, self.column_name, header_style)
            sheet.col(c).width = 256 * self.column_width / 7

        for c, column in enumerate(self.columns):
            for r, row in enumerate(self.rows, start=1):
                sheet.write(r, c, self.value)

        return workbook


class ExportExcelAction(actions.Action):
    label = _("To Excel")
    help_text = _('Export this table as a xls Excel document')
    icon_name = 'csv'
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

        ar.response.update(success=True)
        ar.response.update(open_url=mf.url)

    def render(self, ar, file):
        workbook = ExcelRenderer(ar).render()
        workbook.save(file)

AbstractTable.export_excel = ExportExcelAction()
