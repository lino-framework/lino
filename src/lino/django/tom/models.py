# -*- coding: utf-8 -*-
## Copyright 2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from django import forms
#from django.db import models

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.db import connection
from django.db.models.loading import get_apps, get_app, get_models, get_model, register_models
from django.db.models.query import Q
from django.db.models.expressions import F
from django.db.models.manager import Manager
from django.db.models.base import Model
from django.db.models.aggregates import *
from django.db.models.fields import *
from django.db.models.fields.subclassing import SubfieldBase
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, ManyToManyRel, OneToOneRel
from django.db.models import signals

from django.db.models import permalink



"""
Thanks to 
http://www.pointy-stick.com/blog/2008/10/15/django-tip-poor-mans-model-validation/
"""

class ModelValidationError(Exception):
    def __init__(self, errordict):
        self.errordict=errordict
    def __str__(self):
        return "ModelValidationError (%s)" % \
            ",".join(self.errordict.keys())
    def __getitem__(self,i):
        return self.errordict[i]

class ValidatingModel(Model):
  
    model_form = None
    
    class Meta:
        abstract = True
        
    def validate(self):
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
        self.validate()
        self.before_save()
        super(ValidatingModel, self).save(*args, **kwargs)
        self.after_save()
                    
    def before_save(self):
        pass

    def after_save(self):
        pass
        
    def view(self,response):
        raise NotImimplementedError

    @permalink
    def get_absolute_url(self):
        #return ('lino.django.tom.kernel.', [str(self.id)])
        return (self.__class__.view, [str(self.pk)])
        
