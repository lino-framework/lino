# -*- coding: utf-8 -*-
## Copyright 2009 Luc Saffre
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


from django import forms
from django.db import models
#from lino.django.utils import layouts

"""
Thanks to 
http://www.pointy-stick.com/blog/2008/10/15/django-tip-poor-mans-model-validation/
for the initial idea.
"""

class ModelValidationError(Exception):
    def __init__(self, msg):
        #self.instance = instance
        self.msg = msg
        
    def __str__(self):
        return self.msg
        #~ return "%s %s : %s" % (self.instance.__class__.__name__,
        #~ self.instance.pk, self.msg)
  

#~ class ModelValidationError(Exception):
    #~ def __init__(self, errordict):
        #~ self.errordict=errordict
    #~ def __str__(self):
        #~ return "ModelValidationError (%s)" % \
            #~ ",".join(self.errordict.keys())
    #~ def __getitem__(self,i):
        #~ return self.errordict[i]

class UnusedTomModel(models.Model):
  
    model_form = None
    #quicksearch_fields = None
    #_page_layout = None
    #page_layout_class = layouts.PageLayout
    #detail_reports = None
    
    class Meta:
        abstract = True
        
    def validate_fields(self):
        for field in self._meta.fields:
            meth = getattr(self,"validate_%s" % field.name,None)
            if meth:
                meth()
              
    def validate(self):
        pass
      
        
    def old_validate(self):
        if self.model_form is None: 
            #print "no model_form to validate", self
            return
        #frm = self.model_form(forms.model_to_dict(self))
        #frm = self.model_form(instance=self)
        frm = self.model_form(forms.model_to_dict(self),instance=self)
        if not frm.is_valid():
            #self._errors = frm._errors
            raise ModelValidationError(frm._errors)
        #return frm.is_valid()

    def save(self, *args, **kwargs):
        #print "save:", self
        self.validate_fields()
        self.validate()
        self.before_save()
        super(TomModel,self).save(*args,**kwargs)
        self.after_save()
                    
    def before_save(self):
        pass

    def after_save(self):
        pass
        
    def get_url_path(self):
        return '/instance/%s/%s/%s' % (
          self._meta.app_label,
          self.__class__.__name__, 
          self.pk)
        
        
    def get_actions(self):
        return dict(
          delete = DeleteDialog(self),
        )


class Dialog:
    def view(self,request):
      pass
  
class DeleteDialog(Dialog):
    def __init__(self,instance):
        self.instance = instance
        Dialog.__init__(self)
        
    def view(self,request):
        self.confirm(request,"Are you sure?")
        self.instance.delete()
        
    def confirm(self,request,msg):
        pass
        