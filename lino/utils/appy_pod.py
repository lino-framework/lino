## Copyright 2011-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
An extended `appy.pod` renderer that installs additional functions:

- :meth:`restify <Renderer.restify_func>`: 
  Render a string that is in reStructuredText markup.
- :meth:`html <Renderer.html_func>` :
  Render a string that is in HTML (not XHTML).
- :meth:`table <Renderer.insert_table>`
  Render a Lino Action Request as a table.

"""


import logging
logger = logging.getLogger(__name__)

import os

from appy.pod.renderer import Renderer as AppyRenderer

from lino.utils.restify import restify
from lino.utils.html2xhtml import html2xhtml
from lino.ui import requests as ext_requests
from lino.utils.xmlgen import etree


from django.utils.encoding import force_unicode


#~ from lino.utils.xmlgen import odf
#~ from lxml import etree

OAS = '<office:automatic-styles>'
OFFICE_STYLES = '<office:styles>'

from cStringIO import StringIO
def toxml(node):
    buf = StringIO()
    node.toXml(0, buf)
    return buf.getvalue()


from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties, TableRowProperties, TableCellProperties
#~ from odf.text import P
from odf.element import Text
from odf import text
from odf.table import Table, TableColumns, TableColumn, TableHeaderRows, TableRows, TableRow, TableCell


def html2odftext(e,**kw):
    """
    Convert a :mod:`lino.utils.xmlgen.html` element 
    (e.g. a value of a DisplayField) to an ODF text element.
    Currently it knows only P and B tags, 
    ignoring all other formatting.
    There's probably a better way to do this...
    
    Usage example:
    
    >>> from lino.utils.xmlgen.html import E
    >>> e = E.p("This is a ",E.b("first")," test.")
    >>> print E.tostring(e)
    <p>This is a <b>first</b> test.</p>
    >>> oe = tuple(html2odftext(e))[0]
    >>> print toxml(oe) #doctest: +NORMALIZE_WHITESPACE
    <text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">This 
    is a <text:span text:style-name="Bold Text">first</text:span> test.</text:p>
    
    >>> e = E.p(E.b("This")," is another test.")
    >>> print E.tostring(e)
    <p><b>This</b> is another test.</p>
    
    >>> oe = tuple(html2odftext(e))[0]
    >>> print toxml(oe) #doctest: +NORMALIZE_WHITESPACE
    <text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span 
    text:style-name="Bold Text">This</text:span> is another test.</text:p>
    
    :func:`html2odftext` converts bold text to a span with a 
    style named "Bold Text". That's currently a hard-coded name, and the 
    caller must make sure that a style of that name is defined in the 
    document.
    
    """
    #~ print "20120613 html2odftext()", e.tag, e.text
    if e.tag == 'p': 
        oe = text.P(**kw)
    elif e.tag == 'b':
        oe = text.Span(stylename='Bold Text')
    else:
        #~ raise NotImplementedError("%s (tag %r)" % (e,e.tag))
        oe = text.Span()
    if e.text:
        oe.addText(e.text)
    for child in e:
        for oc in html2odftext(child):
            #~ oe.addElement(oc)
            oe.appendChild(oc)
    yield oe
    if e.tail:
        #~ yield e.tail
        #~ yield text.Span(text=e.tail)
        yield Text(e.tail)



class Renderer(AppyRenderer):
  
    def __init__(self, template, context, result, **kw):
        #~ context.update(appy_renderer=self)
        context.update(restify=self.restify_func)
        context.update(html=self.html_func)
        context.update(table=self.insert_table)
        from lino.extjs import ui
        #~ from lino.ui.extjs3 import urls
        #~ self.ui = urls.ui
        self.extjs_ui = ui
        context.update(ui=ui)
        kw.update(finalizeFunction=self.finalize_func)
        AppyRenderer.__init__(self,template,context,result, **kw)
        #~ self.my_automaticstyles = odf.style.automaticstyles()
        #~ self.my_styles = odf.style.styles()
        self.my_automaticstyles = []
        self.my_styles = []
  
    def restify_func(self,unicode_string,**kw):
        """
        Renders a string in reStructuredText markup by passing it to 
        :func:`lino.utils.restify.restify` to convert it to XHTML, 
        then through :term:`appy.pod`'s built in `xhtml` function.
        
        Without this, users would have to write each time something 
        like::

          do text
          from xhtml(restify(self.body).encode('utf-8'))
            
          do text
          from xhtml(restify(self.body,output_encoding='utf-8'))

        
        """
        if not unicode_string:
            return ''
        
        html = restify(unicode_string,output_encoding='utf-8')
        #~ try:
            #~ html = restify(unicode_string,output_encoding='utf-8')
        #~ except Exception,e:
            #~ print unicode_string
            #~ traceback.print_exc(e)
        #~ print repr(html)
        #~ print html
        return self.renderXhtml(html,**kw)
        #~ return renderer.renderXhtml(html.encode('utf-8'),**kw)
        
    def html_func(self,html,**kw):
        """
        Render a string that is in HTML (not XHTML).
        """
        if not html:
            return ''
        #~ logger.debug("html_func() got:<<<\n%s\n>>>",html)
        #~ print __file__, ">>>"
        #~ print html
        #~ print "<<<", __file__
        html = html2xhtml(html)
        if isinstance(html,unicode):
            # some sax parsers refuse unicode strings. 
            # appy.pod always expects utf-8 encoding.
            # See /blog/2011/0622.
            html = html.encode('utf-8')
        return self.renderXhtml(html,**kw)
        
    def finalize_func(self,fn):
        #~ print "finalize_func()", self.automaticstyles.values()
        #~ fn = os.path.join(fn,'..','content.xml')
        #~ fn = os.path.join(fn,'content.xml')
        self.insert_chunk(fn,'content.xml',OAS,''.join(
          [toxml(e) for e in self.my_automaticstyles]))
        self.insert_chunk(fn,'styles.xml',OFFICE_STYLES,''.join(
          [toxml(e) for e in self.my_styles]))
        
    def insert_chunk(self,root,leaf,insert_marker,chunk):
        """
        post-process specified xml file by inserting a chunk of XML text after the specified insert_marker 
        """
        fn = os.path.join(root,leaf)
        fd = open(fn)
        s = fd.read()
        fd.close()
        chunks = s.split(insert_marker)
        if len(chunks) != 2:
            raise Exception("%s contains more than one %s element ?!" % (fn,insert_marker))
        #~ ss = ''.join(self.my_automaticstyles.values())
        #~ print 20120419, ss
        s = chunks[0] + insert_marker + chunk + chunks[1]
        #~ fd = open('tmp.xml',"w")
        fd = open(fn,"w")
        fd.write(s)
        fd.close()
        #~ raise Exception(fn)
        

    def add_style(self,name,**kw):
        kw.update(name=name)
        #~ e = odf.style.style(odf.style.makeattribs(**kw))
        e = odf.style.add_child(self.my_styles,'style')
        odf.style.update(e,**kw)
        #~ e.style_name = name
        #~ k = e.get('name')
        #~ self.my_styles[name] = e
        return e
        
    def insert_table(self,ar,column_names=None):
        """
        Render an :class:`lino.core.actions.ActionRequest` as an OpenDocument table.
        This is the function that gets called when a template contains a 
        ``do text from table(...)`` statement.
        """
        
        if ar.request is None:
            columns = None
        else:
            columns = [str(x) for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_COLUMNS)]
        
        if columns:
            #~ widths = [int(x) for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_WIDTHS)]
            all_widths = ar.request.REQUEST.getlist(ext_requests.URL_PARAM_WIDTHS)
            hiddens = [(x == 'true') for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_HIDDENS)]
            fields = []
            widths = []
            headers = []
            ah = ar.actor.get_handle(self.extjs_ui)
            for i,cn in enumerate(columns):
                col = None
                for e in ah.list_layout.main.columns:
                    if e.name == cn:
                        col = e
                        break
                if col is None:
                    #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                    #~ raise Exception("No column named %r in %s" % (cn,ah.list_layout.main.columns))
                    raise Exception("No column named %r in %s" % (cn,ar.ah.list_layout.main.columns))
                if not hiddens[i]:
                    fields.append(col.field._lino_atomizer)
                    headers.append(unicode(col.label or col.name))
                    widths.append(int(all_widths[i]))
        else:
            if column_names:
                from lino.core import layouts
                ll = layouts.ListLayout(ar.actor,column_names)
                lh = ll.get_layout_handle(self.extjs_ui)
                columns = lh.main.columns
            else:
                ah = ar.actor.get_handle(self.extjs_ui)
                columns = ah.list_layout.main.columns
                #~ columns = ar.ah.list_layout.main.columns
            #~ fields = ar.ah.store.list_fields
            headers = [unicode(col.label or col.name) for col in columns]
            widths = [(col.width or col.preferred_width) for col in columns]
            fields = [col.field._lino_atomizer for col in columns]

        oh = ar.actor.override_column_headers(ar)
        if oh:
            for i,e in enumerate(columns):
                header = oh.get(e.name,None)
                if header is not None:
                    headers[i] = header
            #~ print 20120507, oh, headers
            
                  
        tw = sum(widths)
        """
        specifying relative widths doesn't seem to work
        (and that's a pity because absolute widths requires a 
        hard-coded table width). 
        """
        use_relative_widths = False
        if use_relative_widths:
            width_specs = ["%d*" % (w*100/tw) for w in widths]
            #~ width_specs = [(w*100/tw) for w in widths]
        else:
            aw = 180 # suppose table width = 18cm = 180mm
            width_specs = ["%dmm" % (aw*w/tw) for w in widths]
        #~ print 20120419, width_specs 
        
        doc = OpenDocumentText()
        def add_style(**kw):
            st = Style(**kw)
            doc.styles.addElement(st)
            self.my_styles.append(st)
            return st

        # create some visible styles
        
        st = add_style(name="Table Contents", family="paragraph",parentstylename="Default")
        st.addElement(ParagraphProperties(numberlines="false", 
            linenumber="0"))
            
        st = add_style(name="Number Cell", family="paragraph",parentstylename="Table Contents")
        st.addElement(ParagraphProperties(numberlines="false", 
            textalign="end", justifysingleword="true",
            linenumber="0"))
        
        dn = "Table Column Header"
        st = self.stylesManager.styles.getStyle(dn)
        if st is None:
            st = add_style(name=dn, family="paragraph",parentstylename="Table Contents")
            st.addElement(ParagraphProperties(numberlines="false", 
                linenumber="0"))
            st.addElement(TextProperties(fontweight="bold"))
        
        dn = "Bold Text"
        st = self.stylesManager.styles.getStyle(dn)
        if st is None:
            st = add_style(name=dn, family="text",parentstylename="Default")
            #~ st = add_style(name=dn, family="text")
            st.addElement(TextProperties(fontweight="bold"))
        
        # create some automatic styles
        
        def add_style(**kw):
            st = Style(**kw)
            doc.automaticstyles.addElement(st)
            self.my_automaticstyles.append(st)
            return st
            
        cell_style = add_style(name="Lino Cell Style",family="table-cell")
        cell_style.addElement(TableCellProperties(
            paddingleft="1mm",paddingright="1mm",
            paddingtop="1mm",paddingbottom="0.5mm",
            border="0.002cm solid #000000"))
            
        header_row_style = add_style(name="Lino Header Row",family="table-row",parentstylename=cell_style)
        header_row_style.addElement(TableRowProperties(backgroundcolor="#eeeeee"))
        
        total_row_style = add_style(name="Lino Total Row",family="table-row",parentstylename=cell_style)
        total_row_style.addElement(TableRowProperties(backgroundcolor="#ffffff"))
        
        table = Table()
        table_columns = TableColumns()
        table.addElement(table_columns)
        table_header_rows = TableHeaderRows()
        table.addElement(table_header_rows)
        table_rows = TableRows()
        table.addElement(table_rows)
        
        # create table columns and automatic table-column styles 
        for i,fld in enumerate(fields):
            #~ print 20120415, repr(fld.name)
            name = str(ar.actor)+"."+fld.name
            cs = add_style(name=name, family="table-column")
            if use_relative_widths:
                cs.addElement(TableColumnProperties(relcolumnwidth=width_specs[i]))
            else:
                cs.addElement(TableColumnProperties(columnwidth=width_specs[i]))
            #~ cs.addElement(TableColumnProperties(useoptimalcolumnwidth='true'))
            #~ k = cs.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = toxml(e)
            #~ doc.automaticstyles.addElement(cs)
            #~ self.my_automaticstyles.append(cs)
            table_columns.addElement(TableColumn(stylename=name))
            
        from lino.ui.extjs3 import ext_store
        def fldstyle(fld):
            if isinstance(fld,ext_store.VirtStoreField):
                fld = fld.delegate
            if isinstance(fld,(
                ext_store.DecimalStoreField,
                ext_store.IntegerStoreField,
                ext_store.RequestStoreField,
                ext_store.AutoStoreField
                )):
                return "Number Cell"
            return "Table Contents"
        
        def value2cell(ar,i,fld,val,style_name,tc):
            #~ text = html2odt.html2odt(fld.value2html(ar,val))
            params = dict()
            #~ if isinstance(fld,ext_store.BooleanStoreField):
                #~ params.update(text=fld.value2html(ar,val))
            #~ else:
                #~ params.update(text=fld.format_value(ar,val))
            #~ params.update(text=fld.format_value(ar,val))
            txt = fld.value2html(ar,val)
            #~ if isinstance(txt,etree.Element): 
            if etree.iselement(txt): 
                chunks = tuple(html2odftext(txt,stylename=style_name))
                assert len(chunks) == 1
                p = chunks[0]
                #~ txt = etree.tostring(txt)
                #~ pass
            else:
                txt = unicode(txt)
            #~ if not isinstance(txt,basestring): 
                #~ raise Exception("Expected Element or basestring, got %r" % txt.__class__)
                params.update(text=txt)
                params.update(stylename=style_name)
                #~ e = fld.value2odt(ar,val)
                p = text.P(**params)
            #~ p.addElement(e)
            #~ yield p
            try:
                tc.addElement(p)
            except Exception,e:
                print 20120614, i, fld, val, e
                
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
            
        sums  = [fld.zero for fld in fields]
          
        for row in ar.data_iterator:
            #~ for grp in ar.group_headers(row):
                #~ raise NotImplementedError()
            tr = TableRow()
            table_rows.addElement(tr)
            
            for i,fld in enumerate(fields):
                #~ tc = TableCell(stylename=CELL_STYLE_NAME)
                tc = TableCell(stylename=cell_style)
                #~ if fld.field is not None:
                v = fld.full_value_from_object(row,ar)
                stylename = fldstyle(fld)
                if v is None:
                    tc.addElement(text.P(stylename=stylename,text=''))
                else:
                    value2cell(ar,i,fld,v,stylename,tc)
                    sums[i] += fld.value2num(v)
                tr.addElement(tc)
                
        if sums != [fld.zero for fld in fields]:
            tr = TableRow(stylename=total_row_style)
            table_rows.addElement(tr)
            for i,fld in enumerate(fields):
                tc = TableCell(stylename=cell_style)
                stylename = fldstyle(fld)
                tc.addElement(text.P(stylename=stylename,
                    text=fld.format_sum(ar,sums,i)))
                tr.addElement(tc)
            

        doc.text.addElement(table)
        return toxml(table)
        #~ if output_file:
            #~ doc.save(output_file) # , True)
        #~ return doc
        
        

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

