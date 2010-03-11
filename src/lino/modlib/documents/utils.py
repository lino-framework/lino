## Copyright 2009-2010 Luc Saffre
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

import os
import logging
import cStringIO

from django.conf import settings
from django.template.loader import render_to_string, get_template, select_template, Context
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _

try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None
    
import lino
from lino import actions

if False:
    try:
        from lino.utils import appy_pod
    except ImportError:
        appy_pod = None

class Printable:
  
    @classmethod
    def setup_report(cls,rpt):
        #~ rpt.add_actions(PrintAction(),PdfAction())
        rpt.add_actions(PdfAction())
        
    def pdf_root(self):
        return os.path.join(settings.MEDIA_ROOT,"pdf_cache")
        
    def pdf_url(self):
        return settings.MEDIA_URL + "/".join(["pdf_cache",self.pdf_filename()])
        
    def pdf_path(self):
        return os.path.join(self.pdf_root(),self.pdf_filename())
        
    def odt_template(self):
        # when using appy_pod
        return os.path.join(os.path.dirname(__file__),
                            'odt',self._meta.db_table)+'.odt'
    def pdf_filename(self):
        return self._meta.db_table + "/" + str(self.pk) + '.pdf'

    def make_pisa_html(self,MEDIA_URL=settings.MEDIA_URL):
        context = dict(
          instance=self,
          title = unicode(self),
          MEDIA_URL = MEDIA_URL,
        )
        template = select_template(self.html_templates())
        return template.render(Context(context))
        
    def get_last_modified_time(self):
        return None
        
    def make_pdf(self):
        filename = self.pdf_path()
        if not filename:
            return
        lino.log.debug("make_pdf(%s) -> %s", self, filename)
        last_modified = self.get_last_modified_time() 
        if last_modified is not None and os.path.exists(filename):
            mtime = os.path.getmtime(filename)
            #~ st = os.stat(filename)
            #~ mtime = st.st_mtime
            mtime = datetime.datetime.fromtimestamp(mtime)
            if mtime >= last_modified:
                lino.log.debug(" -> %s is up to date",filename)
                return
            os.remove(filename)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if False:
            # using appy.pod
            context = dict(instance=self)
            template = self.odt_template()
            appy_pod.process_pod(template,context,filename)
        else:
            # using pisa
            #url = "file:///"+settings.MEDIA_ROOT + os.path.sep
            #url = "file:///"+settings.MEDIA_ROOT.replace('\\','/') + '/'
            url = settings.MEDIA_ROOT.replace('\\','/') + '/'
            html = self.make_pisa_html(MEDIA_URL=url)
            html = html.encode("ISO-8859-1")
            file(filename+'.html','w').write(html)
            result = cStringIO.StringIO()
            h = logging.FileHandler(filename+'.log','w')
            pisa.log.addHandler(h)
            pdf = pisa.pisaDocument(cStringIO.StringIO(html), result)
            pisa.log.removeHandler(h)
            h.close()
            file(filename,'wb').write(result.getvalue())
            if pdf.err:
                raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
            #return result.getvalue()
            
    def view_pdf(self,request):
        self.make_pdf()
        s = open(self.pdf_path()).read()
        return HttpResponse(s,mimetype='application/pdf')
        
    def view_printable(self,request):
        return HttpResponse(self.make_pisa_html())

    def html_templates(self):
        # when using pisa
        return [ '%s_pisa.html' % self.__class__.__name__.lower() ]

    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
class unused_PrintAction(actions.Action):
    name = 'print'
    needs_selection = True
    label = "Print"
    def run_in_dlg(self,dlg):
        row = dlg.selected_rows[0].get_child_instance()
        try:
            html = row.make_pisa_html()
        except Exception,e:
            yield dlg.exception(e).over()
        yield dlg.show_window(
          title="Printable view",
          maximizable=True,
          html=html,
          ).over()
        #context._response.update(html=row.make_pisa_html())
        #return row.view_printable(context.request)

class PdfAction(actions.Action):
    name = 'pdf'
    needs_selection = True
    label = "PDF"
    def run_in_dlg(self,dlg):
        row = dlg.selected_rows[0].get_child_instance()
        try:
            row.make_pdf()
        except Exception,e:
            yield dlg.exception(e).over()
        #lino.log.debug("redirect to", row.pdf_url())
        yield dlg.redirect(row.pdf_url()).over()
        #return row.view_pdf(context.request)


