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
  Render a string in reStructuredText markup.
- :meth:`html <Renderer.html_func>` :
  Render a string that is in HTML (not XHTML).
- :meth:`table <Renderer.insert_table>`
  Render a Lino Action Request as a table.

We wanted to be 
able to insert rst formatted plain text using a simple comment 
like this::

  do text
  from restify(self.body)
    
Without this hack, users would have to write each time something 
like::

  do text
  from xhtml(restify(self.body).encode('utf-8'))
    
  do text
  from xhtml(restify(self.body,output_encoding='utf-8'))


"""


import logging
logger = logging.getLogger(__name__)

import os

from appy.pod.renderer import Renderer as AppyRenderer

from lino.utils.restify import restify
from lino.utils.html2xhtml import html2xhtml
from lino.ui import requests as ext_requests


from django.utils.encoding import force_unicode


from lino.utils.xmlgen import odf
from lxml import etree

def elem2str(e):
    return etree.tostring(e)

OAS = '<office:automatic-styles>'
OFFICE_STYLES = '<office:styles>'

#~ from cStringIO import StringIO
#~ def elem2str(e):
    #~ xml = StringIO()
    #~ e.toXml(0, xml)
    #~ return xml.getvalue()
        



class Renderer(AppyRenderer):
  
    def __init__(self, template, context, result, **kw):
        #~ context.update(appy_renderer=self)
        context.update(restify=self.restify_func)
        context.update(html=self.html_func)
        context.update(table=self.insert_table)
        from lino.ui.extjs3 import urls
        self.ui = urls.ui
        context.update(ui=self.ui)
        kw.update(finalizeFunction=self.finalize_func)
        AppyRenderer.__init__(self,template,context,result, **kw)
        self.my_automaticstyles = odf.style.automaticstyles()
        self.my_styles = odf.style.styles()
  
    def restify_func(self,unicode_string,**kw):
        """
        Renders a string in reStructuredText markup by passing it to 
        :func:`lino.utils.restify.restify` to convert it to XHTML, 
        then through :term:`appy.pod`'s built in `xhtml` function.
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
        return renderer.renderXhtml(html,**kw)
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
        return renderer.renderXhtml(html,**kw)
        
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
        from lino.ui.extjs3 import ext_store
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
            for i,cn in enumerate(columns):
                col = None
                for e in ar.ah.list_layout.main.columns:
                    if e.name == cn:
                        col = e
                        break
                if col is None:
                    #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                    raise Exception("No column named %r in %s" % (cn,ar.ah.list_layout.main.columns))
                if not hiddens[i]:
                    fields.append(col.field._lino_atomizer)
                    headers.append(unicode(col.label or col.name))
                    widths.append(int(all_widths[i]))
        else:
            if column_names:
                from lino.core import layouts
                ll = layouts.ListLayout(ar.actor,column_names)
                list_layout = ll.get_handle(self.ui)
                columns = list_layout.main.columns
            else:
                columns = ar.ah.list_layout.main.columns
            #~ fields = ar.ah.store.list_fields
            headers = [unicode(col.label or col.name) for col in columns]
            widths = [(col.width or col.preferred_width) for col in columns]
            fields = [col.field._lino_atomizer for col in columns]
                  
        tw = sum(widths)
        """
        specifying relative widths doesn't seem to work
        (and that's a pity because absolute widths requires a 
        hard-coded table width)
        """
        use_relative_widths = False
        if use_relative_widths:
            width_specs = ["%d*" % (w*100/tw) for w in widths]
            #~ width_specs = [(w*100/tw) for w in widths]
        else:
            aw = 180 # suppose table width = 18cm = 180mm
            width_specs = ["%dmm" % (aw*w/tw) for w in widths]
        #~ print 20120419, width_specs 
        
        CELL_STYLE_NAME = "Lino Cell Style"
        HEADER_ROW_STYLE_NAME = "Lino Header Row"

        tablecontents = self.add_style("Table Contents", family="paragraph",parent_style_name="Default")
        #~ pp = odf.style.add_child(tablecontents,'paragraph_properties')
        #~ odf.fo.update(pp,margin_right="3pt",margin_left="3pt")
        
        #~ print etree.tostring(tablecontents,pretty_print=True)
            
        numbercell = self.add_style("Number Cell", family="paragraph",parent_style_name="Table Contents")
        pp = odf.style.add_child(numbercell,'paragraph_properties')
        #~ odf.text.update(pp,number_lines="false", line_number="0")
        odf.fo.update(pp,text_align="end", justify_single_word="true")
        
        tableheader = self.add_style("Table Column Header", family="paragraph",parent_style_name="Table Contents")
        p = odf.style.add_child(tableheader,'text_properties')
        odf.fo.update(p,font_weight="bold")
            #~ number_lines="false", 
            #~ line_number="0")
        
        table = odf.table.table()
        table_columns = odf.table.add_child(table,'table_columns')
        table_header_rows = odf.table.add_child(table,'table_header_rows')
        table_rows = odf.table.add_child(table,'table_rows')
        
        st = odf.style.add_child(self.my_automaticstyles,'style',name=CELL_STYLE_NAME,family="table-cell")
        cp = odf.style.add_child(st,'table_cell_properties')
        odf.fo.update(cp,
            padding_left="1mm",padding_right="1mm",
            padding_top="1mm",padding_bottom="0.5mm",
            border="0.002cm solid #000000")
                    
        st = odf.style.add_child(self.my_automaticstyles,'style',name=HEADER_ROW_STYLE_NAME,family="table-row")
        cp = odf.style.add_child(st,'table_row_properties')
        odf.fo.update(cp,background_color="#eeeeee")
        
        for i,fld in enumerate(fields):
            #~ print 20120415, repr(fld.name)
            k = str(ar.actor)+"."+fld.name
            st = odf.style.add_child(self.my_automaticstyles,'style',name=k,family="table-column")
            if use_relative_widths:
                odf.style.add_child(st,'table_column_properties',
                    rel_column_width=width_specs[i])
            else:
                odf.style.add_child(st,'table_column_properties',
                    column_width=width_specs[i])
                    
            #~ cs.addElement(TableColumnProperties(useoptimalcolumnwidth='true'))
            #~ doc.automaticstyles.addElement(cs)
            #~ k = cs.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = elem2str(e)
            #~ self.my_automaticstyles[k] = cs
            odf.table.add_child(table_columns,'table_column',style_name=k)
            
        def fldstyle(fld):
            if isinstance(fld,(
                ext_store.DecimalStoreField,
                ext_store.IntegerStoreField,
                ext_store.AutoStoreField
                )):
                return "Number Cell"
            #~ return tablecontents
            return "Table Contents"
            
        
        def value2cell(ar,i,fld,val,style_name,tc):
            #~ print "20120420 value2cell", val
            #~ text = html2odt.html2odt(fld.value2html(ar,val))
            params = dict()
            if isinstance(fld,ext_store.BooleanStoreField):
                text=fld.value2html(val)
            elif isinstance(fld,ext_store.RequestStoreField):
                #~ params.update(text=force_unicode(val))
                text=fld.format_value(ar,v)
            else:
                text=force_unicode(val)
            #~ params.update(style_name=style.style_name)
            #~ params.update(style_name=odf.style.getnsattr(style,'name'))
            #~ e = fld.value2odt(ar,val)
            e = odf.text.add_child(tc,'p',**params)
            odf.text.update(e,style_name=style_name)
            e.text = text
            #~ print "20120420", etree.tostring(e)
            #~ p = odf.text.P(**odf.text.makeattribs(**params))
            #~ p.addElement(e)
            #~ tc.addElement(p)
            
        # header
        hr = odf.table.add_child(table_header_rows,'table_row',style_name=HEADER_ROW_STYLE_NAME)
        for fld in fields:
            #~ k = str(ar.actor)+"."+fld.name
            tc = odf.table.add_child(hr,'table_cell',style_name=CELL_STYLE_NAME)
            e = odf.text.add_child(tc,'p')
            odf.text.update(e,style_name="Table Column Header")
                #~ style_name=odf.style.getnsattr(tableheader,'name'))
                #~ style_name=odf.style.getnsattr(tableheader,'name'))
                #~ style_name=tableheader.style_name
            e.text = force_unicode(fld.field.verbose_name or fld.name)
            
        sums  = [0 for col in fields]
          
        ar.init_totals(len(fields))
          
        def init_totals(self,count):
            self.sums = [0] * count
            
        def collect_value(self,row,i,value):
            self.sums[i] += value
            
        def group_headers(self,row):
            if False:
                yield None
            
        # data
        for row in ar.data_iterator:
            for grp in ar.group_headers(row):
                raise NotImplementedError()
            tr = odf.table.add_child(table_rows,'table_row')
            #~ tr = TableRow()
            #~ table.addElement(tr)
            
            for i,fld in enumerate(fields):
                #~ k = str(ar.actor)+"."+fld.name
                style_name = fldstyle(fld)
                tc = odf.table.add_child(tr,'table_cell',style_name=CELL_STYLE_NAME)
                #~ tc = TableCell()
                #~ if fld.field is not None:
                v = fld.full_value_from_object(ar,row)
                if v is None:
                    odf.text.add_child(tc,'p',style_name=style_name)
                    #~ odf.text.add_child(tc,'p',style_name=style.style_name,text='')
                    #~ tc.addElement(text.P(stylename=style,text=''))
                else:
                    value2cell(ar,i,fld,v,style_name,tc)
                    #~ fld.value2odt(ar,v,tc,stylename=tablecontents)
                    #~ for e in value2odt(fld,ar,v):
                        #~ tc.addElement(e)
                    ar.collect_value(row,i,fld.value2int(v))
                #~ tr.addElement(tc)
        #~ odf.validate_chunks(table)
        #~ doc.text.addElement(table)
        return elem2str(table)
        #~ if output_file:
            #~ doc.save(output_file) # , True)
        #~ return doc
        
        
        #~ print doc.automaticstyles.tagName
        #~ inserts = renderer.contentParser.env.inserts
        #~ for e in doc.automaticstyles.childNodes:
            #~ k = e.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = elem2str(e)
            #~ self.automaticstyles[k] = elem2str(e)
            #~ inserts[k] = OdInsert(elem2str(e),doc.automaticstyles.tagName)
            #~ print "20120419 added style %r = %r" % (k,e)
        #~ return '<text:p>yo</text:p>'
            
        #~ print "20120419 inserts", renderer.contentParser.env.inserts
        #~ return ''.join([elem2str(n) for n in doc.text.childNodes])
        #~ doc.text.childNodes[0]
        #~ print 20120419, elem2str(doc.text)
        #~ return elem2str(doc.text)
        #~ return elem2str(doc.text)
        
        


    def finalize_func(self,fn):
        #~ print "finalize_func()", self.automaticstyles.values()
        #~ fn = os.path.join(fn,'..','content.xml')
        #~ fn = os.path.join(fn,'content.xml')
        self.insert_chunk(fn,'content.xml',OAS,''.join(
          [elem2str(e) for e in self.my_automaticstyles]))
        self.insert_chunk(fn,'styles.xml',OFFICE_STYLES,''.join(
          [elem2str(e) for e in self.my_styles]))
        
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
        


    def unused_insert_table(self,ar,column_names=None):
        """
        This is where I stopped using :term:`ODFPy`.
        """
        
        from odf.opendocument import OpenDocumentText
        from odf.style import Style, TextProperties, ParagraphProperties
        from odf.style import TableColumnProperties
        #~ from odf.text import P
        from odf import text
        from odf.table import Table, TableColumn, TableRow, TableCell


        #~ from lino.ui.extjs3 import urls
        #~ doc = urls.ui.table2odt(ar)
        
        
        #~ from lino.utils.xmlgen import odf
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
            for i,cn in enumerate(columns):
                col = None
                for e in ar.ah.list_layout.main.columns:
                    if e.name == cn:
                        col = e
                        break
                if col is None:
                    #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                    raise Exception("No column named %r in %s" % (cn,ar.ah.list_layout.main.columns))
                if not hiddens[i]:
                    fields.append(col.field._lino_atomizer)
                    headers.append(unicode(col.label or col.name))
                    widths.append(int(all_widths[i]))
        else:
            if column_names:
                from lino.core import layouts
                ll = layouts.ListLayout(ar.actor,column_names)
                list_layout = ll.get_handle(self.ui)
                columns = list_layout.main.columns
            else:
                columns = ar.ah.list_layout.main.columns
            #~ fields = ar.ah.store.list_fields
            headers = [unicode(col.label or col.name) for col in columns]
            widths = [(col.width or col.preferred_width) for col in columns]
            fields = [col.field._lino_atomizer for col in columns]
                  
        tw = sum(widths)
        """
        specifying relative widths doesn't seem to work
        (and that's a pity because absolute widths requires a 
        hard-coded table width)
        """
        use_relative_widths = False
        if use_relative_widths:
            width_specs = ["%d*" % (w*100/tw) for w in widths]
            #~ width_specs = [(w*100/tw) for w in widths]
        else:
            aw = 180 # suppose table width = 18cm = 180mm
            width_specs = ["%dmm" % (aw*w/tw) for w in widths]
        #~ print 20120419, width_specs 
        
        #~ odf.table2odt(headers,fields,widths,,row2cells)
        
        #~ from lino.utils import html2odt

        #~ doc = OpenDocumentText()
        # Create a style for the table content. One we can modify
        # later in the word processor.
        tablecontents = self.add_style(name="Table Contents", family="paragraph")
        #~ tablecontents = Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(ParagraphProperties(numberlines="false", 
            linenumber="0"))
            
        numbercell = self.add_style(name="Number Cell", family="paragraph")
        #~ tablecontents = Style(name="Table Contents", family="paragraph")
        numbercell.addElement(ParagraphProperties(numberlines="false", 
            textalign="end", justifysingleword="true",
            linenumber="0"))
        #~ doc.my_styles.addElement(tablecontents)
        
        tableheader = self.add_style(name="Table Column Header", family="paragraph")
        tableheader.addElement(ParagraphProperties(numberlines="false", 
            linenumber="0"))
        #~ doc.styles.addElement(tableheader)
        
        table = Table()
        
        for i,fld in enumerate(fields):
            #~ print 20120415, repr(fld.name)
            cs = Style(name=str(ar.actor)+"."+fld.name, family="table-column")
            if use_relative_widths:
                cs.addElement(TableColumnProperties(relcolumnwidth=width_specs[i]))
            else:
                cs.addElement(TableColumnProperties(columnwidth=width_specs[i]))
            #~ cs.addElement(TableColumnProperties(useoptimalcolumnwidth='true'))
            #~ doc.automaticstyles.addElement(cs)
            k = cs.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = elem2str(e)
            self.my_automaticstyles[k] = cs
            table.addElement(TableColumn(stylename=cs))
            
        def fldstyle(fld):
            if isinstance(fld,ext_store.DecimalStoreField):
                return numbercell
            if isinstance(fld,ext_store.IntegerStoreField):
                return numbercell
            if isinstance(fld,ext_store.AutoStoreField):
                #~ print "20120419", elem2str(numbercell)
                return numbercell
            return tablecontents
            
        from lino.ui.extjs3 import ext_store
        
        def value2cell(ar,i,fld,val,style,tc):
            #~ text = html2odt.html2odt(fld.value2html(ar,val))
            params = dict()
            if isinstance(fld,ext_store.BooleanStoreField):
                params.update(text=fld.value2html(val))
            elif isinstance(fld,ext_store.RequestStoreField):
                #~ params.update(text=force_unicode(val))
                params.update(text=fld.format_value(ar,v))
            else:
                params.update(text=force_unicode(val))
            params.update(stylename=style)
            #~ e = fld.value2odt(ar,val)
            p = text.P(**params)
            #~ p.addElement(e)
            #~ yield p
            tc.addElement(p)
            #~ yield P(stylename=tablecontents,text=text)
            
        # header
        hr = TableRow()
        for fld in fields:
            tc = TableCell()
            tc.addElement(text.P(
                stylename=tableheader,
                text=force_unicode(fld.field.verbose_name or fld.name)))
            hr.addElement(tc)
        table.addElement(hr)
            
        sums  = [0 for col in fields]
          
        for row in ar.data_iterator:
            tr = TableRow()
            table.addElement(tr)
            
            for i,fld in enumerate(fields):
                tc = TableCell()
                #~ if fld.field is not None:
                v = fld.full_value_from_object(ar,row)
                style = fldstyle(fld)
                if v is None:
                    tc.addElement(text.P(stylename=style,text=''))
                else:
                    value2cell(ar,i,fld,v,style,tc)
                    #~ fld.value2odt(ar,v,tc,stylename=tablecontents)
                    #~ for e in value2odt(fld,ar,v):
                        #~ tc.addElement(e)
                    sums[i] += fld.value2int(v)
                tr.addElement(tc)

        #~ doc.text.addElement(table)
        return elem2str(table)
        #~ if output_file:
            #~ doc.save(output_file) # , True)
        #~ return doc
        
        
        #~ print doc.automaticstyles.tagName
        #~ inserts = renderer.contentParser.env.inserts
        #~ for e in doc.automaticstyles.childNodes:
            #~ k = e.getAttribute('name')
            #~ renderer.stylesManager.styles[k] = elem2str(e)
            #~ self.automaticstyles[k] = elem2str(e)
            #~ inserts[k] = OdInsert(elem2str(e),doc.automaticstyles.tagName)
            #~ print "20120419 added style %r = %r" % (k,e)
        #~ return '<text:p>yo</text:p>'
            
        #~ print "20120419 inserts", renderer.contentParser.env.inserts
        #~ return ''.join([elem2str(n) for n in doc.text.childNodes])
        #~ doc.text.childNodes[0]
        #~ print 20120419, elem2str(doc.text)
        #~ return elem2str(doc.text)
        #~ return elem2str(doc.text)
        
        
