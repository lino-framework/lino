# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines :class:`AppyRenderer` (a subclass of
:class:`appy.pod.renderer.Renderer`, not of
:class:`lino.core.renderer.Renderer`).


See also :ref:`lino.admin.appy_templates`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
from copy import copy

from appy.pod.renderer import Renderer as OriginalAppyRenderer

from django.utils.encoding import force_unicode
from django.conf import settings

import odf
from odf.opendocument import OpenDocumentText
from odf.style import (Style, TextProperties, ParagraphProperties,
                       TableProperties)
from odf.text import ListStyle
from odf.style import ListLevelProperties
# ~ from odf.style import ListLevelLabelAlignment # ImportError: cannot import name ListLevelLabelAlignment
from odf.style import (TableColumnProperties, TableRowProperties,
                       TableCellProperties)
from odf import text
from odf import office
from odf.table import (Table, TableColumns, TableColumn,
                       TableHeaderRows, TableRows, TableRow, TableCell)

from lino.utils import isiterable
from lino.utils.restify import restify
from lino.utils.html2xhtml import html2xhtml
from lino.utils.html2odf import html2odf, toxml
from lino.utils.xmlgen.html import E

from lino.modlib.extjs.elems import NumberFieldElement


OAS = '<office:automatic-styles>'
OFFICE_STYLES = '<office:styles>'
UL_LIST_STYLE = """\
<style:style style:name="UL_P" style:family="paragraph" style:parent-style-name="Standard" style:list-style-name="UL"/>
<text:list-style style:name="UL">
<text:list-level-style-bullet text:level="1" text:style-name="Bullet_20_Symbols" text:bullet-char="•"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.27cm" fo:text-indent="-0.635cm" fo:margin-left="1.27cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="2" text:style-name="Bullet_20_Symbols" text:bullet-char="◦"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.905cm" fo:text-indent="-0.635cm" fo:margin-left="1.905cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="3" text:style-name="Bullet_20_Symbols" text:bullet-char="▪"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.54cm" fo:text-indent="-0.635cm" fo:margin-left="2.54cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="4" text:style-name="Bullet_20_Symbols" text:bullet-char="•"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="3.175cm" fo:text-indent="-0.635cm" fo:margin-left="3.175cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="5" text:style-name="Bullet_20_Symbols" text:bullet-char="◦"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="3.81cm" fo:text-indent="-0.635cm" fo:margin-left="3.81cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="6" text:style-name="Bullet_20_Symbols" text:bullet-char="▪"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="4.445cm" fo:text-indent="-0.635cm" fo:margin-left="4.445cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="7" text:style-name="Bullet_20_Symbols" text:bullet-char="•"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="5.08cm" fo:text-indent="-0.635cm" fo:margin-left="5.08cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="8" text:style-name="Bullet_20_Symbols" text:bullet-char="◦"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="5.715cm" fo:text-indent="-0.635cm" fo:margin-left="5.715cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="9" text:style-name="Bullet_20_Symbols" text:bullet-char="▪"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="6.35cm" fo:text-indent="-0.635cm" fo:margin-left="6.35cm"/></style:list-level-properties></text:list-level-style-bullet>
<text:list-level-style-bullet text:level="10" text:style-name="Bullet_20_Symbols" text:bullet-char="•"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="6.985cm" fo:text-indent="-0.635cm" fo:margin-left="6.985cm"/></style:list-level-properties></text:list-level-style-bullet>
</text:list-style>
"""


class AppyRenderer(OriginalAppyRenderer):

    """The extended `appy.pod.renderer` used by Lino.

    """

    def __init__(self, ar, template, context, result, **kw):
        self.ar = copy(ar)
        # self.ar.renderer = settings.SITE.kernel.html_renderer
        # self.ar.renderer = settings.SITE.plugins.bootstrap3.renderer
        self.ar.renderer = settings.SITE.plugins.jinja.renderer
        #~ context.update(appy_renderer=self)
        context.update(restify=self.restify_func)
        context.update(html=self.html_func)
        context.update(jinja=self.jinja_func)
        context.update(table=self.insert_table)
        context.update(as_odt=self.as_odt)
        context.update(story=self.insert_story)
        #~ context.update(html2odf=html2odf)
        context.update(ehtml=html2odf)
        context.update(toxml=toxml)
        #~ from lino.extjs import ui
        #~ self.extjs_ui = ui
        context.update(ui=settings.SITE.kernel)
        context.update(settings=settings)
        context.update(sc=settings.SITE.site_config)
        if False:
            context.update(settings.SITE.modules)
            # 20150810 removed above line because this "feature"
            # caused the name `jinja` defined above to be overridden.
        kw.update(finalizeFunction=self.finalize_func)
        OriginalAppyRenderer.__init__(self, template, context, result, **kw)
        #~ self.my_automaticstyles = odf.style.automaticstyles()
        #~ self.my_styles = odf.style.styles()
        self.my_automaticstyles = []
        self.my_styles = []

    def jinja_func(self, template_name, **kwargs):

        #saved_renderer = self.ar.renderer
        try:
            if not '.' in template_name:
                template_name += '.html'
            #~ printable = self.contentParser.env.context.get('this',None)
            #~ print 20130910, settings.SITE.jinja_env
            env = settings.SITE.plugins.jinja.renderer.jinja_env
            template = env.get_template(template_name)
            #~ print 20130910, template, dir(self)
            html = template.render(self.contentParser.env.context)
            #self.ar.renderer = saved_renderer
            return self.html_func(html)
            #~ print 20130910, html
            #~ return self.renderXhtml(html,**kw)
        except Exception as e:
            #self.ar.renderer = saved_renderer
            import traceback
            traceback.print_exc(e)

    def restify_func(self, unicode_string, **kw):
        """

        """
        if not unicode_string:
            return ''

        html = restify(unicode_string, output_encoding='utf-8')
        #~ try:
            #~ html = restify(unicode_string,output_encoding='utf-8')
        #~ except Exception,e:
            #~ print unicode_string
            #~ traceback.print_exc(e)
        #~ print repr(html)
        #~ print html
        return self.renderXhtml(html, **kw)
        #~ return renderer.renderXhtml(html.encode('utf-8'),**kw)

    def html_func(self, html, **kw):
        """
        Render a string that is in HTML (not XHTML).
        """
        if not html:
            return ''
        if E.iselement(html):
            html = E.tostring(html)
        try:
            html = html2xhtml(html)
        except Exception as e:
            print 20150923, e
        # logger.debug("20141210 html_func() got:<<<\n%s\n>>>", html)
        # print __file__, ">>>"
        # print html
        # print "<<<", __file__
        if isinstance(html, unicode):
            # some sax parsers refuse unicode strings.
            # appy.pod always expects utf-8 encoding.
            # See /blog/2011/0622.
            html = html.encode('utf-8')
            #~ logger.info("20120726 html_func() %r",html)
        return self.renderXhtml(html, **kw)

    def finalize_func(self, fn):
        #~ print "finalize_func()", self.automaticstyles.values()
        #~ fn = os.path.join(fn,'..','content.xml')
        #~ fn = os.path.join(fn,'content.xml')
        #~ if not self.stylesManager.styles.getStyle('UL'):
            #~ self.insert_chunk(fn,'content.xml',OAS,UL_LIST_STYLE)
        self.insert_chunk(fn, 'content.xml', OAS, ''.join(
            [toxml(n).decode('utf-8') for n in self.my_automaticstyles]))
        self.insert_chunk(fn, 'styles.xml', OFFICE_STYLES, ''.join(
            [toxml(n).decode('utf-8') for n in self.my_styles]))

    def insert_chunk(self, root, leaf, insert_marker, chunk):
        """
        post-process specified xml file by inserting a chunk of XML text after the specified insert_marker
        """
        #~ insert_marker = insert_marker.encode('utf-8')
        #~ chunk = chunk.encode('utf-8')
        fn = os.path.join(root, leaf)
        fd = open(fn)
        s = fd.read().decode('utf-8')
        fd.close()
        chunks = s.split(insert_marker)
        if len(chunks) != 2:
            raise Exception("%s contains more than one %s element ?!" %
                            (fn, insert_marker))
        #~ ss = ''.join(self.my_automaticstyles.values())
        #~ print 20120419, ss
        s = chunks[0] + insert_marker + chunk + chunks[1]
        #~ fd = open('tmp.xml',"w")
        fd = open(fn, "w")
        #~ fd.write(s)
        fd.write(s.encode('utf-8'))
        fd.close()
        #~ raise Exception(fn)

    def add_style(self, name, **kw):
        kw.update(name=name)
        #~ e = odf.style.style(odf.style.makeattribs(**kw))
        e = odf.style.add_child(self.my_styles, 'style')
        odf.style.update(e, **kw)
        #~ e.style_name = name
        #~ k = e.get('name')
        #~ self.my_styles[name] = e
        return e

    def story2odt(self, story, *args, **kw):
        "Yield a sequence of ODT chunks (as utf8 encoded strings)."
        from lino.core.actors import Actor
        from lino.core.tables import TableRequest
        for item in story:
            if E.iselement(item):
                yield toxml(html2odf(item))
            elif isinstance(item, type) and issubclass(item, Actor):
                sar = self.ar.spawn(item, *args, **kw)
                yield self.insert_table(sar)
            elif isinstance(item, TableRequest):
                # logger.info("20141211 story2odt %s", item)
                yield self.insert_table(item)
            elif isiterable(item):
                for i in self.story2odt(item, *args, **kw):
                    yield i
            else:
                raise Exception("Cannot handle %r" % item)

    def insert_story(self, story):
        chunks = tuple(self.story2odt(story))
        return str('').join(chunks)
        
    def as_odt(self, obj):
        return obj.as_appy_pod_xml(self)

    def insert_table(self, *args, **kw):
        """
        This is the function that gets called when a template contains a
        ``do text from table(...)`` statement.
        """
        if True:
            return self.insert_table_(*args, **kw)
        else:
            #~ since i cannot yet tell appy_pod to alert me when there is an
            #~ exception, here at least i write it to the logger
            try:
                s = self.insert_table_(*args, **kw)
            except Exception as e:
                logger.warning("Exception during insert_table(%s):" % args[0])
                logger.exception(e)
                raise
            s = s.decode('utf-8')
            #~ logger.info("""\
#~ 20130423 appy_pod.Renderer.insert_table(%s) inserts =======
#~ %s
#~ =======""", args[0], s)
            return s

    def insert_table_(self, ar, column_names=None, table_width=180):
        ar.setup_from(self.ar)
        columns, headers, widths = ar.get_field_info(column_names)
        widths = map(int, widths)
        tw = sum(widths)
        # specifying relative widths doesn't seem to work (and that's
        # a pity because absolute widths requires us to know the
        # table_width).
        use_relative_widths = False
        if use_relative_widths:
            width_specs = ["%d*" % (w * 100 / tw) for w in widths]
        else:
            width_specs = ["%dmm" % (table_width * w / tw) for w in widths]

        doc = OpenDocumentText()

        def add_style(**kw):
            st = Style(**kw)
            doc.styles.addElement(st)
            self.my_styles.append(st)
            return st

        table_style_name = str(ar.actor)
        st = add_style(name=table_style_name, family="table",
                       parentstylename="Default")
        st.addElement(
            TableProperties(align="margins", maybreakbetweenrows="0"))

        # create some *visible* styles

        st = add_style(name="Table Contents", family="paragraph",
                       parentstylename="Default")
        st.addElement(ParagraphProperties(numberlines="false",
                                          linenumber="0"))

        st = add_style(name="Number Cell", family="paragraph",
                       parentstylename="Table Contents")
        st.addElement(ParagraphProperties(
            numberlines="false",
            textalign="end", justifysingleword="true",
            linenumber="0"))

        dn = "Table Column Header"
        st = self.stylesManager.styles.getStyle(dn)
        if st is None:
            st = add_style(name=dn, family="paragraph",
                           parentstylename="Table Contents")
            st.addElement(
                ParagraphProperties(numberlines="false", linenumber="0"))
            st.addElement(TextProperties(fontweight="bold"))

        dn = "Bold Text"
        st = self.stylesManager.styles.getStyle(dn)
        if st is None:
            st = add_style(name=dn, family="text", parentstylename="Default")
            #~ st = add_style(name=dn, family="text")
            st.addElement(TextProperties(fontweight="bold"))

        if False:
            dn = "L1"
            st = self.stylesManager.styles.getStyle(dn)
            if st is None:
                st = ListStyle(name=dn)
                doc.styles.addElement(st)
                p = ListLevelProperties(
                    listlevelpositionandspacemode="label-alignment")
                st.addElement(p)
                #~ label-followed-by="listtab" text:list-tab-stop-position="1.27cm" fo:text-indent="-0.635cm" fo:margin-left="1.27cm"/>
                p.addElement(ListLevelLabelAlignment(labelfollowedby="listtab",
                                                     listtabstopposition="1.27cm",
                                                     textindent="-0.635cm",
                                                     marginleft="1.27cm"
                                                     ))
                self.my_styles.append(st)

                #~ list_style = add_style(name=dn, family="list")
                bullet = text.ListLevelStyleBullet(
                    level=1, stylename="Bullet_20_Symbols", bulletchar=u"•")
                #~ bullet = text.ListLevelStyleBullet(level=1,stylename="Bullet_20_Symbols",bulletchar=u"*")
                #~ <text:list-level-style-bullet text:level="1" text:style-name="Bullet_20_Symbols" text:bullet-char="•">
                st.addElement(bullet)

        # create some automatic styles

        def add_style(**kw):
            st = Style(**kw)
            doc.automaticstyles.addElement(st)
            self.my_automaticstyles.append(st)
            return st

        cell_style = add_style(name="Lino Cell Style", family="table-cell")
        cell_style.addElement(TableCellProperties(
            paddingleft="1mm", paddingright="1mm",
            paddingtop="1mm", paddingbottom="0.5mm",
            border="0.002cm solid #000000"))

        header_row_style = add_style(
            name="Lino Header Row", family="table-row",
            parentstylename=cell_style)
        header_row_style.addElement(
            TableRowProperties(backgroundcolor="#eeeeee"))

        total_row_style = add_style(
            name="Lino Total Row", family="table-row",
            parentstylename=cell_style)
        total_row_style.addElement(
            TableRowProperties(backgroundcolor="#ffffff"))

        table = Table(name=table_style_name, stylename=table_style_name)
        table_columns = TableColumns()
        table.addElement(table_columns)
        table_header_rows = TableHeaderRows()
        table.addElement(table_header_rows)
        table_rows = TableRows()
        table.addElement(table_rows)

        # create table columns and automatic table-column styles
        for i, fld in enumerate(columns):
            #~ print 20120415, repr(fld.name)
            name = str(ar.actor) + "." + fld.name
            cs = add_style(name=name, family="table-column")
            if use_relative_widths:
                cs.addElement(
                    TableColumnProperties(relcolumnwidth=width_specs[i]))
            else:
                cs.addElement(
                    TableColumnProperties(columnwidth=width_specs[i]))
            #~ cs.addElement(TableColumnProperties(useoptimalcolumnwidth='true'))
            #~ k = cs.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = toxml(e)
            #~ doc.automaticstyles.addElement(cs)
            #~ self.my_automaticstyles.append(cs)
            table_columns.addElement(TableColumn(stylename=name))

        def fldstyle(fld):
            #~ if isinstance(fld,ext_store.VirtStoreField):
                #~ fld = fld.delegate
            if isinstance(fld, NumberFieldElement):
                return "Number Cell"
            return "Table Contents"

        def value2cell(ar, i, fld, val, style_name, tc):
            txt = fld.value2html(ar, val)

            p = text.P(stylename=style_name)
            html2odf(txt, p)

            try:
                tc.addElement(p)
            except Exception as e:
                logger.warning("20120614 addElement %s %s %r : %s",
                               i, fld, val, e)
                #~ print 20120614, i, fld, val, e

            #~ yield P(stylename=tablecontents,text=text)

        # create header row
        #~ hr = TableRow(stylename=HEADER_ROW_STYLE_NAME)
        hr = TableRow(stylename=header_row_style)
        table_header_rows.addElement(hr)
        for h in headers:
        #~ for fld in fields:
            #~ tc = TableCell(stylename=CELL_STYLE_NAME)
            tc = TableCell(stylename=cell_style)
            tc.addElement(text.P(
                stylename="Table Column Header",
                #~ text=force_unicode(fld.field.verbose_name or fld.name)))
                text=force_unicode(h)))
            hr.addElement(tc)

        sums = [fld.zero for fld in columns]

        for row in ar.data_iterator:
            #~ for grp in ar.group_headers(row):
                #~ raise NotImplementedError()
            tr = TableRow()

            has_numeric_value = False

            for i, fld in enumerate(columns):
                #~ tc = TableCell(stylename=CELL_STYLE_NAME)
                tc = TableCell(stylename=cell_style)
                #~ if fld.field is not None:
                v = fld.field._lino_atomizer.full_value_from_object(row, ar)
                stylename = fldstyle(fld)
                if v is None:
                    tc.addElement(text.P(stylename=stylename, text=''))
                else:
                    value2cell(ar, i, fld, v, stylename, tc)

                    nv = fld.value2num(v)
                    if nv != 0:
                        sums[i] += nv
                        has_numeric_value = True
                    #~ sums[i] += fld.value2num(v)
                tr.addElement(tc)

            if has_numeric_value or not ar.actor.hide_zero_rows:
                table_rows.addElement(tr)

        if not ar.actor.hide_sums:
            if sums != [fld.zero for fld in columns]:
                tr = TableRow(stylename=total_row_style)
                table_rows.addElement(tr)
                for i, fld in enumerate(columns):
                    tc = TableCell(stylename=cell_style)
                    stylename = fldstyle(fld)
                    p = text.P(stylename=stylename)
                    e = fld.format_sum(ar, sums, i)
                    html2odf(e, p)
                    tc.addElement(p)
                    #~ if len(txt) != 0:
                        #~ msg = "html2odf() returned "
                        #~ logger.warning(msg)
                    #~ txt = tuple(html2odf(fld.format_sum(ar,sums,i),p))
                    #~ assert len(txt) == 1
                    #~ tc.addElement(text.P(stylename=stylename,text=txt[0]))
                    tr.addElement(tc)

        doc.text.addElement(table)
        return toxml(table)
        #~ if output_file:
            # ~ doc.save(output_file) # , True)
        #~ return doc


