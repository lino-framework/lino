# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangosite.dbutils import models_by_base
from lino.core.tables import VirtualTable
from lino.core.fields import displayfield, virtualfield
from lino.utils.xmlgen.html import E
from lino.mixins import Controllable
from lino import dd


class OrphanedControllables(VirtualTable):

    column_names = "owner_model invalid_pk"

    @classmethod
    def get_data_rows(self, ar):
        for M in models_by_base(Controllable):
            for obj in M.objects.filter(owner_id__isnull=False):
                if obj.owner is None:
                    yield obj

    @displayfield(_("Model"))
    def owner_model(self, obj, ar):
        # return E.p(unicode(obj.__class__))
        return dd.full_model_name(obj.__class__)
    
    @virtualfield(models.IntegerField(_("Primary key")))
    def invalid_pk(self, obj, ar):
        return obj.owner_id

    

    
