# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines the model mixins :class:`Sequenced` and
:class:`Hierarchical`.

A `Sequenced` is something which has a sequence number and thus a sort
order which can be manipulated by the user using actions
:class:`MoveUp` and :class:`MoveDown`.

:class:`Hierarchical` is a :class:`Sequenced` with a `parent` field.

"""

from __future__ import unicode_literals
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


from lino.core import actions
from lino.core import fields
from lino.core.utils import navinfo
from etgen.html import E
from lino.utils import AttrDict
from lino.utils import join_elems

from .duplicable import Duplicable, Duplicate


class MoveByN(actions.Action):
    """Move this row N rows upwards or downwards.

    This action is available on any :class:`Sequenced` object as
    :attr:`Sequenced.MoveByN`.

    It is currently only used by React to allow for drag and drop reording.

    """

    # label = _("Up")
    # label = "\u2191" thin arrow up
    # label = "\u25b2" # triangular arrow up
    # label = "\u25B2"  # ▲ Black up-pointing triangle
    # label = "↑"  #
    custom_handler = True
    # icon_name = 'arrow_up'
    #~ icon_file = 'arrow_up.png'
    readonly = False
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        if ar.data_iterator is None:
            return False
        if not super(MoveByN, self).get_action_permission(ar, obj, state):
            return False
        if ar.data_iterator.count() == 0:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.seqno += int(ar.request.GET['seqno'])
        obj.seqno_changed(ar)
        # obj.full_clean()
        obj.save()
        kw = dict()
        kw.update(refresh_all=True)
        kw.update(message=_("Reordered."))
        ar.success(**kw)



class MoveUp(actions.Action):
    """Move this row one row upwards.

    This action is available on any :class:`Sequenced` object as
    :attr:`Sequenced.move_up`.

    """

    # label = _("Up")
    # label = "\u2191" thin arrow up
    # label = "\u25b2" # triangular arrow up
    label = "\u25B2"  # ▲ Black up-pointing triangle
    # label = "↑"  #
    custom_handler = True
    # icon_name = 'arrow_up'
    #~ icon_file = 'arrow_up.png'
    readonly = False

    def get_action_permission(self, ar, obj, state):
        if ar.data_iterator is None:
            return False
        if not super(MoveUp, self).get_action_permission(ar, obj, state):
            return False
        if ar.data_iterator.count() == 0:
            return False
        if ar.data_iterator[0] == obj:
            return False
        # print("20161128", obj.seqno, ar.data_iterator.count())
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.seqno -= 1
        obj.seqno_changed(ar)
        # obj.full_clean()
        obj.save()
        kw = dict()
        kw.update(refresh_all=True)
        kw.update(message=_("Moved up."))
        ar.success(**kw)


class MoveDown(actions.Action):
    """Move this row one row downwards.

    This action is available on any :class:`Sequenced` object as
    :attr:`Sequenced.move_down`.

    """
    # label = _("Down")
    label = "↓"
    # label = "\u25bc" # triangular arrow down
    # label = "\u2193"
    label = "\u25BC"  # ▼ Black down-pointing triangle
    # icon_name = 'arrow_down'
    custom_handler = True
    #~ icon_file = 'arrow_down.png'
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
        obj.seqno += 1
        # obj.seqno = obj.seqno + 1
        obj.seqno_changed(ar)
        # obj.full_clean()
        obj.save()
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
        qs = obj.get_siblings().filter(seqno__gt=seqno).order_by('-seqno')
        for s in qs:
            #~ print '20120605 duplicate inc', s.seqno, s.account
            s.seqno += 1
            s.save()
        kw.update(seqno=seqno+1)
        return super(DuplicateSequenced, self).run_from_code(ar, **kw)


from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Sequenced(Duplicable):
    """Mixin for models that have a field :attr:`seqno` containing a
    "sequence number".

    .. attribute:: seqno

        The sequence number of this item with its parent.

    .. method:: duplicate

        Create a duplicate of this object and insert the new object
        below this one.

    .. attribute:: move_up

        Exchange the :attr:`seqno` of this item and the previous item.

    .. attribute:: move_down

        Exchange the :attr:`seqno` of this item and the next item.

    .. attribute:: move_buttons

        Displays buttons for certain actions on this row:

        - :attr:`move_up` and :attr:`move_down`
        - duplicate

    """

    move_action_names = ('move_up', 'move_down', 'duplicate')
    """The names of the actions to display in the `move_buttons`
    column.

    Overridded by :class:`lino.modlib.notify.models.Widget` where the
    duplicate button would be irritating.

    """

    class Meta(object):
        abstract = True
        ordering = ['seqno']

    # seqno = models.IntegerField(_("Seq.No."), blank=True, null=False)
    seqno = models.IntegerField(_("No."), blank=True, null=False)

    duplicate = DuplicateSequenced()
    """The :class:`DuplicateSequenced` action for this object.

    """

    move_up = MoveUp()
    """The :class:`MoveUp` action on this object.

    """

    move_down = MoveDown()
    """The :class:`MoveDown` action on this object.

    """

    move_by_n = MoveByN()
    """The :class:`MoveByN` action on this object.

    """


    def __str__(self):
        return str(_("Row # %s") % self.seqno)

    def get_siblings(self):
        """Return a Django Queryset with all siblings of this, or `None` if
        this is a root element which cannot have any siblings.

        Siblings are all objects that belong to a same sequence.
        This is needed for automatic management of the `seqno` field.

        The queryset will of course include `self`.

        The default implementation uses a global sequencing by
        returning all objects of `self`'s model.

        A common case for overriding this method is when numbering
        restarts for each master.  For example if you have a master
        model `Product` and a sequenced slave model `Property` with a
        ForeignKey field `product` which points to the Product, then
        you'll define::

          class Property(dd.Sequenced):

              def get_siblings(self):
                  return Property.objects.filter(
                      product=self.product)

        Overridden e.g. in
        :class:`lino_xl.lib.thirds.models.Third`
        or
        :class:`lino_welfare.modlib.debts.models.Entry`.

        """
        return self.__class__.objects.order_by('seqno')

    def set_seqno(self):
        """
        Initialize `seqno` to the `seqno` of eldest sibling + 1.
        """
        qs = self.get_siblings().order_by('seqno')
        if qs is None:  # TODO: remove this as it is no longer used (?)
            self.seqno = 0
        else:
            n = qs.count()
            if n == 0:
                self.seqno = 1
            else:
                last = qs[n - 1]
                self.seqno = last.seqno + 1

    def full_clean(self, *args, **kw):
        if not self.seqno:
            self.set_seqno()
        super(Sequenced, self).full_clean(*args, **kw)

        # if hasattr(self, 'amount'):
        #     logger.info("20151117 Sequenced.full_clean a %s", self.amount)
        #     logger.info("20151117  %s", self.__class__.mro())
        # if hasattr(self, 'amount'):
        #     logger.info("20151117 Sequenced.full_clean b %s", self.amount)

    def seqno_changed(self, ar):
        """If the user manually assigns a seqno."""
        #get siblings list
        qs = self.get_siblings().order_by('seqno').exclude(
            id=self.id)

        # print("20170615 qs is", qs)
        # old_self = qs.get(id=self.id)
        # qs = qs.exclude(id=self.id)

        # if old_self.seqno != self.seqno:
        seq_no = 1
        n = 0

        for i in qs:
            if seq_no == self.seqno:
                seq_no += 1

            if i.seqno != seq_no:
                i.seqno = seq_no
                # if diff
                i.save()
                n += 1

            seq_no += 1
            
        ar.success(message=_("Renumbered {} of {} siblings.").format(
            n, qs.count()))
        ar.set_response(refresh_all=True)
        
    @fields.displayfield(_("Move"))
    def move_buttons(obj, ar):
        if ar is None:
            return ''
        actor = ar.actor
        l = []
        state = None  # TODO: support a possible state?
        for n in obj.move_action_names:
            ba = actor.get_action_by_name(n)
            if ba.get_row_permission(ar, obj, state):
                l.append(ar.renderer.action_button(obj, ar, ba))
                l.append(' ')
        return E.p(*l)


Sequenced.set_widget_options('move_buttons', width=5)
Sequenced.set_widget_options('seqno', hide_sum=True)


class Hierarchical(Duplicable):
    """Abstract model mixin for things that have a "parent" and
    "siblings".

    Pronounciation: [hai'ra:kikl]

    """
    class Meta(object):
        abstract = True

    parent = fields.ForeignKey('self',
                               verbose_name=_("Parent"),
                               null=True, blank=True,
                               related_name='children')

    @fields.displayfield(_("Children"))
    def children_summary(self, ar):
        if ar is None:
            return ''
        elems = [ar.obj2html(ch) for ch in self.children.all()]
        elems = join_elems(elems, sep=', ')
        return E.p(*elems)

    def get_siblings(self):
        if self.parent:
            return self.parent.children.all()
        return self.__class__.objects.filter(parent__isnull=True)

    #~ def save(self, *args, **kwargs):
        #~ super(Hierarchical, self).save(*args, **kwargs)
    def full_clean(self, *args, **kwargs):
        p = self.parent
        while p is not None:
            if p == self:
                raise ValidationError("Cannot be your own ancestor")
            p = p.parent
        super(Hierarchical, self).full_clean(*args, **kwargs)

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

    def get_parental_line(self):
        """Return an ordered list of all ancestors of this instance.  

        The last element of the list is this.
        A top-level project is its own root.

        """
        obj = self
        tree = [obj]
        while obj.parent is not None:
            obj = obj.parent
            if obj in tree:
                raise Exception("Circular parent")
            tree.insert(0, obj)
        return tree

    def whole_clan(self):
        """Return a set of this instance and all children and grandchildren.

        """
        # TODO: go deeper but check for circular references
        clan = set([self])
        l1 = self.__class__.objects.filter(parent=self)
        if l1.count() == 0:
            return clan
        clan |= set(l1)
        l2 = self.__class__.objects.filter(parent__in=l1)
        if l2.count() == 0:
            return clan
        clan |= set(l2)
        l3 = self.__class__.objects.filter(parent__in=l2)
        if l3.count() == 0:
            return clan
        clan |= set(l3)
        # print 20150421, projects
        return clan

