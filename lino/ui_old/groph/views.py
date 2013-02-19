from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

from lino.utils.xmlgen import html as xghtml

class Index(View):

    def get(self, request, *args, **kwargs):
        ui = settings.LINO.groph_ui
        print repr(settings.LINO.modules.lino.Home.default_action.get_window_layout())
        actor = settings.LINO.modules.lino.Home
        ah = actor.get_handle(ui)
        print ah
        a = actor.default_action
        ar = actor.request(ui,request,a)
        print ar
        html = '\n'.join([ln for ln in self.html_page(ar,*args,**kwargs)])
        return HttpResponse(html)

    def html_page(self,ar,*args,**kw):
        wl = ar.action.get_window_layout()
        print wl.main
        lh = wl.get_layout_handle(ar.ui)
        print lh.main.__html__(ar)
        
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        yield '<title id="title">%s</title>' % settings.LINO.title
        
        user = ar.get_user()  # request.subst_user or request.user
        menu = settings.LINO.get_site_menu(self,user.profile)
        yield '</head><body>'
        
        yield menu.as_html(ar)
        story = []
        #~ story.append(xghtml.E.p(str(menu)))
        #~ story.append(xghtml.E.p(str(args)))
        #~ story.append(xghtml.E.p(str(kw)))
        e = xghtml.E.div(*story,id='body')
        yield xghtml.E.tostring(e)
        yield lh.main.__html__(ar)
        
        yield "</body></html>"
        
