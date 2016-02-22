"""Database models for `lino.modlib.print_pisa`.

"""
from future import standard_library
standard_library.install_aliases()

import logging
import os
import io
from django.conf import settings
from ho import pisa
from lino.core.web import extend_context
from lino.utils.appy_pod import PrintTableAction
from lino.core.tables import AbstractTable
from lino.utils.media import TmpMediaFile
from lino.utils.xmlgen import html as xghtml
from django.utils.translation import ugettext_lazy as _


class PrintTableActionPisa(PrintTableAction):
    template_name = "table.pisa.html"

    def run_from_ui(self, ar, **kw):
        # Prepare tmp file
        mf = TmpMediaFile(ar, self.target_file_format)
        settings.SITE.makedirs_if_missing(os.path.dirname(mf.name))

        # Render
        self.render(ar, mf.name)

        ar.response.update(success=True)
        ar.response.update(open_url=mf.url)

    def as_html_table(self, ar):
        t = xghtml.Table()
        ar.dump2html(t, ar.data_iterator)

        return xghtml.E.tostring(t.as_element())

    def render(self, ar, output_file):
        context = {
            'action': self,
            'ar': ar,
            'as_html_table': self.as_html_table,
        }

        extend_context(context)

        template = settings.SITE.plugins.jinja.renderer.jinja_env.get_template(
            self.template_name)
        html = template.render(**context).encode('utf-8')

        with open(output_file + '.html', "w") as file:
            file.write(html)

        result = io.StringIO()
        h = logging.FileHandler(output_file + '.log', 'w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(
            io.StringIO(html), result, encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()

        with open(output_file, 'wb') as file:
            file.write(result.getvalue())
            file.close()

        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)


class PortraitPrintTableActionPisa(PrintTableActionPisa):
    label = _("Table (portrait)")
    sort_index = -9
    template_name = "table-portrait.pisa.html"

AbstractTable.as_pdf = PrintTableActionPisa()
AbstractTable.as_pdf_p = PortraitPrintTableActionPisa()
