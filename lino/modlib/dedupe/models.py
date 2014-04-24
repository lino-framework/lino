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

"""Defines a virtual table :class:`SimilarPersons`, and overrides the
`submit_insert` action of `contacts.Person` with a specialized variant
which checks for duplicate persons.

The current implementation of the detection algorithm is rather
primitive.  We might one day add another table with NYSIIS or SOUNDEX
strings.

Examples and test cases in :ref:`welfare.tested.pcsw`.

"""

from __future__ import unicode_literals

# import fuzzy
# fuzzy.nysiis()


import logging
logger = logging.getLogger(__name__)


from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino.core.actions import SubmitInsert

contacts = dd.resolve_app('contacts')


class SimilarPersons(dd.VirtualTable):
    """Shows a slave table of persons that are "similar" to a given master
    instance (and therefore are potential duplicates).

    """
    label = _("Similar Persons")
    # slave_grid_format = 'html'
    slave_grid_format = 'summary'

    class Row:

        def __init__(self, master, slave):
            self.master = master
            self.slave = slave

        def summary_row(self, ar):
            yield ar.obj2html(self.slave)

        def __unicode__(self):
            return unicode(self.slave)

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        for o in self.find_similar_instances(mi):
            yield self.Row(mi, o)

    @classmethod
    def get_words(self, obj):
        s1 = set()
        for s in (obj.last_name, obj.first_name):
            for word in s.split():
                s1.add(word)
        s2 = set()
        for n in s1:
            for word in n.split('-'):
                s2.add(word)
        return s2
    
    @classmethod
    def find_similar_instances(self, obj):
        """This is Lino's default algorithm for finding similar humans in a
        database. It is rather simplistic. To become more smart, we
        might add helper tables with soundex copies of the names.

        """
        qs = contacts.Person.objects.exclude(pk=obj.pk)
        for w in self.get_words(obj):
            # logger.info("20140222 find_similar_instances word %s", w)
            flt = Q(last_name__icontains=w) | Q(first_name__icontains=w)
            qs = qs.filter(flt)
        # logger.info("20140222 find_similar_instances %s", qs.query)
        return qs

    @dd.displayfield(_("Other"))
    def other(self, obj, ar):
        return ar.obj2html(obj.slave)


class CheckedSubmitInsert(SubmitInsert):
    """Specialized variant of `SubmitInsert` which checks for duplicate
persons.

    """

    def run_from_ui(self, ar, **kw):
        obj = ar.create_instance_from_request()

        def ok(ar2):
            self.save_new_instance(ar2, obj)

        qs = SimilarPersons.find_similar_instances(obj)
        if qs.count() > 0:
            msg = _("There are %d %s with similar name:") % (
                qs.count(), qs.model._meta.verbose_name_plural)
            for other in qs[:4]:
                msg += '<br/>' + unicode(other)

            msg += '<br/>'
            msg += _("Are you sure you want to create a new "
                     "%(model)s named %(name)s?") % dict(
                         model=qs.model._meta.verbose_name,
                         name=obj.get_full_name())
            
            ar.confirm(ok, msg)
        else:
            ok(ar)


@dd.receiver(dd.pre_analyze)
def install_submit_insert(sender, **kw):
    sender.modules.contacts.Person.define_action(
        submit_insert=CheckedSubmitInsert())

