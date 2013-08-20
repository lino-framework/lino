from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

class A(dd.RowAction):
    
    label = _("a")
    
    def run_from_ui(self,obj,ar,**kw):
        return ar.success("Called a() on %s" % obj)

class M(dd.Model):
    a = A()
    @dd.action(_("m"))
    def m(self,ar,**kw):
        return ar.success("Called m() on %s" % self)
        
class T(dd.Table):
    model = M
    
    @dd.action(_("t"))
    def t(obj,ar,**kw):
        return ar.success("Called t() on %s" % obj)

class S1(T):
    pass

class S2(T):
    m = None
    t = None

class S3(S2):
    b = A()
