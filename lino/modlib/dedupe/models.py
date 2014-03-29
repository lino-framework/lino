# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""Defines a virtual table SimilarPersons.

Current implementation is very primitive: same last_name and same
first letter of first_name.

We plan to add another table with NYSIIS or SOUNDEX strings.

"""

from __future__ import unicode_literals

# import fuzzy
# fuzzy.nysiis()


import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from lino import dd


def find_similar_instances(obj, truncate, *fieldnames):
    qs = obj.__class__.objects.exclude(pk=obj.pk)
    # qs = obj.__class__.objects.all()
    # flt = models.Q(last_name__icontains=obj.last_name)

    # v = obj.first_name[:2]
    # flt &= models.Q(first_name__istartswith=v)

    v = obj.first_name[:2]
    return qs.filter(
        last_name__icontains=obj.last_name, first_name__istartswith=v)

    # for k in fieldnames:
    #     v = getattr(obj, k)
    #     if truncate is not None:
    #         v = v[:truncate]
    #     flt = flt | models.Q(**{k + '__icontains': v})
    # return qs.filter(flt)


class SimilarPersons(dd.VirtualTable):
    label = _("Similar Persons")
    slave_grid_format = 'html'

    class Row:

        def __init__(self, master, slave):
            self.master = master
            self.slave = slave

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        # others = set()

        for o in find_similar_instances(mi, None, 'last_name', 'first_name'):
            # if not o in others:
            #     others.add(o)
            yield self.Row(mi, o)

        # for o in find_similar_instances(mi, 5, 'last_name'):
        #     if not o in others:
        #         others.add(o)
        #         yield self.Row(mi, o)
        
    @dd.displayfield(_("Other"))
    def other(self, obj, ar):
        return ar.obj2html(obj.slave)
