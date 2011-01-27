## Copyright 2009-2011 Luc Saffre
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

"coretools may not be used in models modules (but well during lino_site set up)."

from django.db.models import loading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from lino.core import actors

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
def get_slave(model,name):
    rpt = actors.get_actor(name)
    if rpt is None: 
        return None
    if rpt.master is not ContentType:
        assert issubclass(model,rpt.master), "%s.master is %r, must be subclass of %r" % (name,rpt.master,model)
    return rpt
    #~ rpt = generic_slaves.get(name,None)
    #~ if rpt is not None:
        #~ return rpt
    #~ for b in (model,) + model.__bases__:
        #~ d = getattr(b,"_lino_slaves",None)
        #~ if d:
            #~ rpt = d.get(name,None)
            #~ if rpt is not None:
                #~ return rpt

def get_model_report(model):
    return model._lino_model_report

def get_unbound_meth(cl,name):
    meth = getattr(cl,name,None)
    if meth is not None:
        return meth
    for b in cl.__bases__:
        meth = getattr(b,name,None)
        if meth is not None:
            return meth
            
def data_elems(model):
    """Yields names that can be used as column_names of a Report.
    """
    meta = model._meta
    #~ for f in meta.fields: yield f.name
    #~ for f in meta.many_to_many: yield f.name
    #~ for f in meta.virtual_fields: yield f.name
    for f in meta.fields: 
        if f.editable:
            yield f
    for f in meta.many_to_many: yield f
    for f in meta.virtual_fields: yield f
    # todo: for slave in self.report.slaves
    
def get_data_elem(model,name):
    try:
        return model._meta.get_field(name)
    except models.FieldDoesNotExist,e:
        pass
    rpt = get_slave(model,name)
    if rpt is not None: return rpt
    m = get_unbound_meth(model,name)
    if m is not None: return m
    
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf

