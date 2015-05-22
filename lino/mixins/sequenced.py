# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines the model mixins :class:`Sequenced` and
:class:`Hierarizable`.

A `Sequenced` is something which has a sequence number and thus a sort
order which can be manipulated by the user using actions
:class:`MoveUp` and :class:`MoveDown`.

:class:`Hierarizable` is a :class:`Sequenced` with a `parent` field.

.. autosummary::

"""

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino.core import actions
from lino.core import fields
from lino.core.utils import navinfo
from lino.utils.xmlgen.html import E
from lino.utils import AttrDict

from .duplicable import Duplicable, Duplicate


class MoveUp(actions.Action):
    """Move current row one upwards. This action is available on any
:class:`Sequenced` object as :attr:`Sequenced.move_up`.

    """

    # label = _("Up")
    # label = "\u2191" thin arrow up
    # label = "\u25b2" # triangular arrow up
    label = "↑"  #
    custom_handler = True
    # icon_name = 'arrow_up'
    #~ icon_file = 'arrow_up.png'
    help_text = _("Move this row one row upwards")
    readonly = False

    def get_action_permission(self, ar, obj, state):
        if ar.data_iterator is None:
            return False
        if not super(MoveUp, self).get_action_permission(ar, obj, state):
            return False
        #~ logger.info("20130927 %r", ar.data_iterator.__class__)
        if ar.data_iterator.count() == 0:
            return False
        if ar.data_iterator[0] == obj:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.swap_seqno(ar, -1)
        #~ obj.move_up()
        kw = dict()
        #~ kw.update(refresh=True)
        kw.update(refresh_all=True)
        kw.update(message=_("Moved up."))
        ar.success(**kw)


class MoveDown(actions.Action):
    """Move current row one downwards. This action is available on any
:class:`Sequenced` object as :attr:`Sequenced.move_down`.

    """
    # label = _("Down")
    label = "↓"
    # ~ label = "\u25bc" # triangular arrow down
    #~ label = "\u2193"
    # icon_name = 'arrow_down'
    custom_handler = True
    #~ icon_file = 'arrow_down.png'
    help_text = _("Move this row one row downwards")
    readonly = False

    def get_action_permission(self, ar, obj, state):
        if ar.data_iterator is None:
            return False
        if not super(MoveDown, self).get_action_permission(ar, obj, state):
            return False
        if ar.data_iterator.count() == 0:
            return False
        if ar.data_iterator[ar.data_iterator.count() - 1] == obj:
            return False
        #~ if obj.__class__.__name__=='Entry' and obj.seqno == 25:
            #~ print 20130706, ar.data_iterator.count(), ar.data_iterator
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.swap_seqno(ar, 1)
        #~ obj.move_down()
        kw = dict()
        #~ kw.update(refresh=True)
        kw.update(refresh_all=True)
        kw.update(message=_("Moved down."))
        ar.success(**kw)


class DuplicateSequenced(Duplicate):
    """Duplicate this row."""
    def run_from_code(self, ar, **kw):
        obj = ar.selected_rows[0]

        #~ print '20120605 duplicate', self.seqno, self.account
        seqno = obj.seqno
        qs = obj.get_siblings().filter(seqno__gte=seqno).reverse()
        if qs is None:
            raise Exception(
                "20121227 TODO: Tried to duplicate a root element?")
        for s in qs:
            #~ print '20120605 duplicate inc', s.seqno, s.account
            s.seqno += 1
            s.save()
        kw.update(seqno=seqno)
        return super(DuplicateSequenced, self).run_from_code(ar, **kw)


class Sequenced(Duplicable):
    """Abstract base class for models that have a field `seqno`
    containing a "sequence number".

    """

    class Meta:
        abstract = True
        ordering = ['seqno']

    seqno = models.IntegerField(_("Seq.No."), blank=True, null=False)

    duplicate = DuplicateSequenced()
    """The :class:`DuplicateSequenced` action for this object.

    """

    move_up = MoveUp()
    """The :class:`MoveUp` action on this object.

    """

    move_down = MoveDown()
    """The :class:`MoveDown` action on this object.

    """

    def __unicode__(self):
        return unicode(_("Row # %s") % self.seqno)

    def get_siblings(self):
        """Return a Django Queryset with all siblings of this,
        or `None` if this is a root element which cannot have any siblings.

        Siblings are all objects that belong to a same sequence.
        This is needed for automatic management of the `seqno` field.

        The queryset will of course include `self`.
        The default implementation uses a global sequencing
        by returning all objects of `self`'s model.

        A common case for overriding this method is when numbering
        restarts for each master.  For example if you have a master
        model `Product` and a sequenced slave model `Property` with a
        ForeignKey field `product` which points to the Product, then
        you'll define::

          class Property(dd.Sequenced):

              def get_siblings(self):
                  return Property.objects.filter(
                      product=self.product).order_by('seqno')

        Overridden e.g. in
        :class:`lino.modlib.thirds.models.Third`
        or
        :class:`lino_welfare.modlib.debts.models.Entry`.

        """
        return self.__class__.objects.order_by('seqno')

    def set_seqno(self):
        """
        Initialize `seqno` to the `seqno` of eldest sibling + 1.
        """
        qs = self.get_siblings()
        if qs is None:
            self.seqno = 0
        else:
            n = qs.count()
            if n == 0:
                self.seqno = 1
            else:
                last = qs[n - 1]
                self.seqno = last.seqno + 1

    def full_clean(self, *args, **kw):
        if self.seqno is None:
            self.set_seqno()
        super(Sequenced, self).full_clean(*args, **kw)

    def swap_seqno(self, ar, offset):
        """
        Move this row "up or down" within its siblings
        """
        #~ qs = self.get_siblings()
        qs = ar.data_iterator
        if qs is None:
            return
        nav = AttrDict(**navinfo(qs, self))
        if not nav.recno:
            return
        new_recno = nav.recno + offset
        if new_recno <= 0:
            return
        if new_recno > qs.count():
            return
        other = qs[new_recno - 1]
        prev_seqno = other.seqno
        other.seqno = self.seqno
        self.seqno = prev_seqno
        self.save()
        other.save()

    @fields.displayfield(_("Move"), preferred_width=5)
    def move_buttons(obj, ar):
        """
        Displays the buttons for this row and this user.
        """
        actor = ar.actor
        l = []
        state = None  # TODO: support a possible state?
        for n in ('move_up', 'move_down'):
            ba = actor.get_action_by_name(n)
            if ba.get_bound_action_permission(ar, obj, state):
                l.append(ar.renderer.action_button(obj, ar, ba))
                l.append(' ')
        return E.p(*l)


class Hierarizable(Sequenced):
    """Abstract model mixin for things that have a "parent" and
    "siblings".

    """
    class Meta:
        abstract = True

    parent = models.ForeignKey('self',
                               verbose_name=_("Parent"),
                               null=True, blank=True,
                               related_name='children')

    def get_siblings(self):
        if self.parent:
            return self.parent.children.all()
        return self.__class__.objects.filter(parent__isnull=True)

    #~ def save(self, *args, **kwargs):
        #~ super(Hierarizable, self).save(*args, **kwargs)
    def full_clean(self, *args, **kwargs):
        p = self.parent
        while p is not None:
            if p == self:
                raise ValidationError("Cannot be your own ancestor")
            p = p.parent
        super(Hierarizable, self).full_clean(*args, **kwargs)

    def is_parented(self, other):
        if self == other:
            return True
        p = self.parent
        while p is not None:
            if p == other:
                return True
            p = p.parent

    def get_parents(self):
        rv = []
        p = self.parent
        while p is not None:
            rv.insert(p)
            p = p.parent
        return rv


