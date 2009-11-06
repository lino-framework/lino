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

from django.test import TestCase
from lino.utils.validatingmodel import TomModel, ModelValidationError
from lino.utils.reports import Report
from lino.utils.render import ViewReportRenderer
from django.db import models
from django.forms.models import modelform_factory, formset_factory
from django.conf import settings

from lino.apps.documents import models as documents

class Document(documents.AbstractDocument):
    pass
    
class DocumentsTest(TestCase):
  
    def test01(self):
        pass