# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

u"""
Defines the model mixin :class:`Duplicable`.
"duplicable" [du'plikəblə] means "able to produce a duplicate ['duplikət],['du:plikeit]".
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor

from lino import dd
from lino.core.modeltools import obj2str


#~ def duplicate_row(obj,**kw):
    #~ obj.pk = None
    #~ for k,v in kw.items():
        #~ setattr(obj,k,v)
    #~ return obj

#~ from lino.core.coretools import get_data_elem

class Duplicable(dd.Model):
    """
    Adds a row action "Duplicate" which duplicates (creates a clone of) 
    the object it was called on.
    
    Subclasses may override :meth:`on_duplicate` to customize the default 
    behaviour,
    which is to copy all fields except the primary key 
    and all related objects that are duplicable.
    
    """
    class Meta:
        abstract = True
        
    #~ duplicated_fields = None
    
    #~ @classmethod
    #~ def site_setup(self,site):
        #~ """
        #~ Converts the magic model attribute `duplicate_fields` from a string
        #~ to a list of tuples (name,data element). We do this during site_setup 
        #~ (1) to identify typo's or wrong field names directly at startup
        #~ and (2) to save lookups during each request.
        #~ """
        #~ if self.duplicated_fields is not None:
            #~ if isinstance(self.duplicated_fields,basestring):
                #~ l = []
                #~ for name in self.duplicated_fields.split():
                    #~ de = get_data_elem(self,name)
                    #~ if de is None:
                        #~ raise Exception(
                            #~ "Unknown data element name %r for %s" % (
                              #~ name,self))
                    #~ l.append((name,de))
                #~ self.duplicated_fields = l
      
        
    
    @dd.action(_("Duplicate"),sort_index=60,show_in_workflow=False)
    def duplicate_row(self,ar,**kw):
        #~ if not isinstance(ar,actions.ActionRequest):
            #~ raise Exception("Expected and ActionRequest but got %r" % ar)
        #~ related = dict()
        for f in self._meta.fields:
            if not f.primary_key:
                kw[f.name] = getattr(self,f.name)
        #~ for m2m in self._meta.many_to_many:
            #~ print m2m
        #~ print self._lino_ddh.fklist
        related = []
        for m,fk in self._lino_ddh.fklist:
            #~ related[fk] = m.objects.filter(**kw)
            if getattr(m,'allow_cascaded_delete',False):
                related.append((fk,m.objects.filter(**{fk.name:self})))
            #~ if issubclass(m,Duplicable):
                #~ related[fk.related_name] = getattr(self,fk.name)
                #~ related[fk.name] = getattr(self,fk.rel.related_name)
        #~ print related
        #~ raise Exception("20120612")
        #~ for name,de in self.duplicated_fields:
            #~ if isinstance(de,models.Field):
                #~ kw[name] = getattr(self,name)
            #~ elif isinstance(de,ForeignRelatedObjectsDescriptor):
                #~ ro = getattr(self,name)
                #~ related[de] = ro
                #~ # print de.related.parent_model
                #~ # print de.related.model
                #~ # print de.related.opts
                #~ # print de.related.field
                #~ # print de.related.name
                #~ # print de.related.var_name
                #~ # print '---'
            #~ else:
                #~ raise Exception("20120612 Cannot handle %r" % de)
                
        #~ print 20120608, kw
        new = ar.create_instance(**kw)
        #~ new = duplicate_row(self)
        #~ new.on_duplicate(ar)
        new.on_duplicate(ar,None)
        #~ m = getattr(new,'on_duplicate',None)
        #~ if m is not None:
            #~ m(ar,None)
        #~ print 20120612, obj2str(new)
        new.save(force_insert=True)
        
        for fk,qs in related:
            for obj in qs:
                obj.pk = None
                setattr(obj,fk.name,new)
                if isinstance(obj,Duplicable):
                    obj.on_duplicate(ar,new)
                #~ m = getattr(obj,'on_duplicate',None)
                #~ if m is not None:
                    #~ m(ar,new)
                obj.save()
        
        #~ for de,rm in related.items():
            #~ # rm is the RelatedManager
            #~ for obj in rm.all():
                #~ obj.pk = None
                #~ setattr(obj,de.related.field.name,new)
                #~ m = getattr(obj,'on_duplicate',None)
                #~ if m is not None:
                    #~ m(ar,new)
                #~ obj.save()
                
                
        kw = dict()
        kw.update(refresh=True)
        kw.update(message=_("Duplicated %(old)s to %(new)s.") % dict(old=self,new=new))
        #~ kw.update(new_status=dict(record_id=new.pk))
        kw.update(goto_record_id=new.pk)
        return ar.success_response(**kw)
        
    def on_duplicate(self,ar,master):
        pass
  
