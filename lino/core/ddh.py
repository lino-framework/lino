# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models


class DisableDeleteHandler():
    """Used to find out whether a known object can be deleted or not.

    Lino's default behaviour is to forbit deletion if there is any
    other object in the database that refers to this. To implement
    this, Lino installs a `DisableDeleteHandler` instance on each
    model in an attribute `_lino_ddh` during kernel startup.

    """

    def __init__(self, model):
        self.model = model
        self.fklist = []

    def add_fk(self, rel_model, fk):
        # called from kernel.
        for m, fld in self.fklist:
            if rel_model is m:
                # avoid duplicate entries caused by MTI children
                return
        self.fklist.append((rel_model, fk))

    def __str__(self):
        return ','.join([m.__name__ + '.' + fk.name for m, fk in self.fklist])

    def disable_delete_on_object(self, obj):
        # logger.info("20101104 called %s.disable_delete(%s)", obj, self)
        for m, fk in self.fklist:
            if fk.name in m.allow_cascaded_delete:
                continue
            if fk.null and fk.rel.on_delete == models.SET_NULL:
                continue
            n = m.objects.filter(**{fk.name: obj}).count()
            if n:
                return obj.delete_veto_message(m, n)
        kernel = settings.SITE.kernel
        # print "20141208 generic related objects for %s:" % obj
        for gfk, fk_field, qs in kernel.get_generic_related(obj):
            if gfk.name in qs.model.allow_cascaded_delete:
                continue
            if fk_field.null:  # a nullable GFK is no reason to veto
                continue
            n = qs.count()
            # print "20141208 - %s %s %s" % (
            #     gfk.model, gfk.name, qs.query)
            if n:
                return obj.delete_veto_message(qs.model, n)
        return None

