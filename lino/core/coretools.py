## Copyright 2009-2012 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)


from django.db.models import loading
from django.db import models
from django.conf import settings
from django.utils.importlib import import_module
from django.contrib.contenttypes.models import ContentType
from lino.core import actors
from lino.utils import get_class_attr

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
def get_slave(model,name):
    """Return the named report, knowing that it is a 
    slave of the specified `model`. 
    If name has no app_label specified, use the model's app_label.
    """
    if not '.' in name:
        name = model._meta.app_label + '.' + name
    rpt = actors.get_actor(name)
    if rpt is None: 
        return None
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
    if not hasattr(model,'_lino_default_table'):
        raise Exception("%r has no _lino_default_table" % model)
    return model._lino_default_table

def get_unbound_meth(cl,name):
    raise Exception("replaced by lino.utils.get_class_attr")
    
    
def get_data_elem(model,name):
    #~ logger.info("20120202 get_data_elem %r,%r",model,name)
    try:
        return model._meta.get_field(name)
    except models.FieldDoesNotExist,e:
        pass
        
    #~ s = name.split('.')
    #~ if len(s) == 1:
        #~ mod = import_module(model.__module__)
        #~ rpt = getattr(mod,name,None)
    #~ elif len(s) == 2:
        #~ mod = getattr(settings.LINO.modules,s[0])
        #~ rpt = getattr(mod,s[1],None)
    #~ else:
        #~ raise Exception("Invalid data element name %r" % name)
    
    v = get_class_attr(model,name)
    if v is not None: return v
    
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf

