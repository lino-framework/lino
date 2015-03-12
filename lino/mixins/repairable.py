# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for handling automatic data reparation.

It is about "repairing" data which has some kind of "logical"
invalidity.  The data is "technically" valid (there is no database
constraint to test it).

Such invalid data can be due to bugs in previous versions, due to
import from old data, ...

This is a generic solution to write such conditions and manage their
reparation.

Tested by :mod:`lino_welfare.projects.std.test_beid`.

.. autosummary::

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd, rt, _


class Repairable(dd.Model):
    """Mixin for models which have a :meth:`repairdata` method.

    """

    class Meta:
        abstract = True

    def repairdata(self, really=False):
        """Repair any repairable problem. If `really` is False, just
        simulate. Return or yield a list of strings which explain what
        has (or would have) been done.

        """
        return []

    @classmethod
    def get_repairable_objects(cls):
        """Return a queryset of the objects that are to be asked whether they
        need reparation. The default implementation returns all
        objects. Override this if only a subset of your Model
        instances have a chance of reparation.

        """
        return cls.objects.all()


def flatten(iterable):
    for msg in iterable:
        if isinstance(msg, basestring):
            yield msg
        else:
            for msg2 in flatten(msg):
                yield msg2


def repairdata(really=False):
    """Loop over all repairable database objects and
    run the :meth:`repair
    <Repairable.repair>` method on each of them.
    
    Yield one line of text per object which had at least one repair
    message.

    This is what :manage:`repairdata` command calls to do its work.

    """
        
    for m in rt.models_by_base(Repairable):
        for obj in m.get_repairable_objects():
            l = list(flatten(obj.repairdata(really=really)))
            msg = '. '.join(l)
            if msg:
                yield "{0} : {1}".format(obj, msg.strip())
