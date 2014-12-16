# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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
        self.fklist.append((rel_model, fk))

    def __str__(self):
        return ','.join([m.__name__ + '.' + fk.name for m, fk in self.fklist])

    def disable_delete_on_object(self, obj):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        #~ h = getattr(self.model,'disable_delete',None)
        #~ if h is not None:
            #~ msg = h(obj,ar)
        #~     if msg is not None:
            #~     return msg

        def veto(obj, m, n):
            msg = _(
                "Cannot delete %(self)s "
                "because %(count)d %(refs)s refer to it."
            ) % dict(
                self=obj, count=n,
                refs=m._meta.verbose_name_plural
                or m._meta.verbose_name + 's')
            #~ print msg
            return msg

        for m, fk in self.fklist:
            if not fk.name in m.allow_cascaded_delete:
                n = m.objects.filter(**{fk.name: obj}).count()
                if n:
                    return veto(obj, m, n)
        kernel = settings.SITE.kernel
        # print "20141208 generic related objects for %s:" % obj
        for gfk, qs in kernel.get_generic_related(obj):
            if gfk.name in qs.model.allow_cascaded_delete:
                continue
            if gfk.name in qs.model.allow_stale_generic_foreignkey:
                continue
            n = qs.count()
            # print "20141208 - %s %s %s" % (
            #     gfk.model, gfk.name, qs.query)
            if n:
                return veto(obj, qs.model, n)
        return None


