# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the :class:`Polymorphic` model mixin.
See :doc:`/dev/mti`.

"""
from builtins import object
from builtins import str

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from etgen.html import E

from lino.core import fields
from lino.core import model
from lino.core.actions import Action
from lino.core.signals import pre_remove_child, pre_add_child  # , on_add_child
from lino.core.utils import models_by_base
from lino.core.utils import resolve_model
from lino.utils import mti


class ChildAction(Action):

    readonly = False
    show_in_bbar = False

    def __init__(self, child_model, *args, **kw):
        self.child_model = child_model
        super(ChildAction, *args, **kw)

    def get_action_name(self):
        return self.name_prefix + self.child_model.__name__.lower()

    def attach_to_actor(self, actor, name):
        self.child_model = resolve_model(self.child_model)
        self._label = self.child_model._meta.verbose_name
        return super(ChildAction, self).attach_to_actor(actor, name)

    def get_child(self, obj):
        """Returns the MTI child in `self.child_model` if it exists, otherwise
return None.

        """
        try:
            return self.child_model.objects.get(pk=obj.pk)
        except self.child_model.DoesNotExist:
            return None

    def run_from_ui(self, ar, **kw):
        assert len(ar.selected_rows) == 1
        self.run_on_row(ar.selected_rows[0], ar)


class DeleteChild(ChildAction):
    name_prefix = 'del_'

    def get_action_permission(self, ar, obj, state):
        if self.get_child(obj) is None:
            return False
        return super(DeleteChild, self).get_action_permission(ar, obj, state)

    def run_on_row(self, obj, ar):
    
        if ar is not None:
            pre_remove_child.send(
                sender=obj, request=ar.request,
                child=self.child_model)
        mti.delete_child(obj, self.child_model, ar)
        ar.set_response(refresh=True)


class InsertChild(ChildAction):

    name_prefix = 'ins_'

    def get_action_permission(self, ar, obj, state):
        parent_link_field = self.child_model._meta.parents.get(
            obj.__class__, None)
        if parent_link_field is None:
            return False
        if self.get_child(obj) is not None:
            return False

        return super(InsertChild, self).get_action_permission(ar, obj, state)

    def run_on_row(self, obj, ar):
        if ar is not None:
            pre_add_child.send(
                sender=obj, request=ar.request,
                child=self.child_model)
        mti.insert_child(obj, self.child_model, full_clean=True)
        ar.set_response(refresh=True)


class Polymorphic(model.Model):
    """Mixin for models that use Multiple Table Inheritance to implement
    polymorphism.

    Subclassed e.g. by :class:`lino_xl.lib.contacts.Partner`:
    the recipient of an invoice can be a person, a company, a client,
    a job provider, an employee..., and a given partner can be both a
    person and an employee at the same time.

    Note that not every usage of Multiple Table Inheritance means
    polymorphism. For example `lino_xl.lib.ledger.models.Voucher`
    has a pointer to the journal which knows which specialization to
    use, so a given voucher has always exactly one specialization.

    .. attribute:: mti_navigator

        A virtual field which defines buttons for switching between the
        different views.

    Usage examples in :doc:`/dev/mti` and :doc:`/dev/lets/index`.

    """
    class Meta(object):
        abstract = True

    _mtinav_models = None

    @classmethod
    def on_analyze(cls, site):
        super(Polymorphic, cls).on_analyze(site)
        if cls._mtinav_models is None:
            models = list(models_by_base(cls))

            # TODO: it would be nice to have them sorted in some
            # understandable way, but that's not trivial. First
            # attempts are not satisfying:
            #
            # def f(a, b):
            #     level = 0
            #     if b in a.__bases__:
            #         level -= a.__bases__.index(b)
            #     if a in b.__bases__:
            #         level += b.__bases__.index(a)
            #     return level
            # models.sort(f)

            cls._mtinav_models = tuple(models)

            def add(m, cl):
                a = cl(m)
                cls.define_action(**{a.get_action_name(): a})

            for m in cls._mtinav_models:
                add(m, DeleteChild)
                add(m, InsertChild)

    def get_mti_child(self, *args):
        """Return the specified specialization or `None`.

        For example if you have two models `Place(Model)` and
        `Restaurant(Place)` and a `Place` instance ``p`` which is
        *not* also a Restaurant, then `p.get_mti_child('restaurant')`
        will return `None`.

        """
        for a in args:
            try:
                return getattr(self, a)
            except ObjectDoesNotExist:
                pass
        #~ return self

    def disable_delete(self, ar=None):
        """Overrides :meth:`lino.core.model.Model.disable_delete`.

        In case of polymorphy, the user can ask to delete any MTI
        instance of a polymorphic entity. Deleting one instance will
        delete all other instances as well.

        Before deleting one polymorphic instance, we ask all other
        instances for their vetos.

        Cascade-related objects are deleted independently of the
        instance that initiated deletion.

        """
        # ask all other forms of this for vetos:
        for m in self._mtinav_models:
            if m is not self.__class__:
                obj = mti.get_child(self, m)
                if obj is not None:
                    ignore_models = set(self._mtinav_models)
                    ignore_models.remove(m)
                    msg = m._lino_ddh.disable_delete_on_object(
                        obj, ignore_models)
                    if msg is not None:
                        return msg

        # Now ask my own model, ignoring all other forms because they
        # have been asked.
        ignore_models = set(self._mtinav_models)
        ignore_models.remove(self.__class__)
        return self.__class__._lino_ddh.disable_delete_on_object(
            self, ignore_models=ignore_models)

    def get_mti_buttons(self, ar):
        """"""
        elems = []
        if ar is None:
            return elems
        sep = None
        for m in self._mtinav_models:
            item = None
            if self.__class__ is m:
                item = [E.b(str(m._meta.verbose_name))]
            else:
                obj = mti.get_child(self, m)
                if obj is None:
                    # parent link field
                    p = m._meta.parents.get(self.__class__, None)
                    if p is not None:
                        item = [str(m._meta.verbose_name)]
                        k = InsertChild.name_prefix + m.__name__.lower()
                        ba = ar.actor.get_action_by_name(k)
                        if ba and ba.get_row_permission(ar, self, None):
                            # btn = ar.row_action_button(self, ba, _("+"))
                            btn = ar.row_action_button(self, ba, _(u"➕"))
                            # Heavy Plus Sign U+2795
                            # btn = ar.row_action_button(self, ba,
                            #                            icon_name='add')
                            item += [" [", btn, "]"]

                else:
                    da = obj.get_detail_action(ar)
                    if da is not None:
                        item = [ar.obj2html(obj, m._meta.verbose_name)]
                        # no DeleteChild for my parents
                        if self.__class__ in m.mro():
                            k = DeleteChild.name_prefix + m.__name__.lower()
                            ba = ar.actor.get_action_by_name(k)
                            if ba and ba.get_row_permission(ar, self, None):
                                btn = ar.row_action_button(self, ba, _(u"❌"))
                                # Cross Mark U+274C
                                item += [" [", btn, "]"]

            if item is not None:
                if sep is None:
                    sep = ', '
                else:
                    elems.append(sep)
                elems += item
        return elems

    @fields.displayfield(_("See as "))
    def mti_navigator(self, ar):
        buttons = self.get_mti_buttons(ar)
        return E.span(*buttons)

    def obj2href(self, ar, *args, **kwargs):
        # a = super(Polymorphic, self).get_detail_action(ar)
        a = self.get_detail_action(ar)
        if a is not None:
            return super(Polymorphic, self).obj2href(ar, *args, **kwargs)
        for m in self._mtinav_models:
            if m is not self.__class__:
                obj = mti.get_child(self, m)
                if obj is not None:
                    if obj.get_detail_action(ar) is not None:
                        return obj.obj2href(ar, *args, **kwargs)
        return ''

