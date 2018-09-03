# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from builtins import object
from django.contrib.contenttypes.models import *

from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from lino.api import dd
from lino.core.gfks import gfk2lookup

from .fields import GenericForeignKey, GenericForeignKeyIdField


class Controllable(dd.Model):

    """Mixin for models that are "controllable" by another database object.

    Defines three fields :attr:`owned_type`, :attr:`owned_id` and
    :attr:`owned`. And a class attribute :attr:`owner_label`.

    For example in :mod:`lino.modlibs.cal`, the owner of a Task or Event
    is some other database object that caused the task's or event's
    creation.

    Or in :mod:`lino.modlib.sales` and :mod:`lino.modlib.purchases`,
    an invoice may cause one or several Tasks to be automatically generated
    when a certain payment mode is specified.

    Controllable objects are "governed" or "controlled" by their
    controller (stored in a field called :attr:`owner`): If the
    controller gets modified, it may decide to delete or modify some
    or all of her controlled objects.

    Non-automatic tasks always have an empty :attr:`owner` field.
    Some fields are read-only on an automatic Task because it makes no
    sense to modify them.

    .. attribute:: owner
    .. attribute:: owner_id
    .. attribute:: owner_type

    """
    # Translators: will also be concatenated with '(type)' '(object)'
    owner_label = _('Controlled by')
    """Deprecated. This is (and always was) being ignored. Use
    :meth:`update_controller_field` instead.
    The labels (`verbose_name`) of the fields `owned_type`, `owned_id`
    and `owned` are derived from this attribute which may be overridden by
    subclasses.
    """

    controller_is_optional = True
    """Deprecated. This is (and always was) being ignored. Use
    :meth:`update_controller_field` instead.

    """

    class Meta(object):
        abstract = True

    owner_type = dd.ForeignKey(
        ContentType,
        editable=True,
        blank=True, null=True,
        verbose_name=format_lazy(u"{} {}", owner_label, _('(type)')))
    

    owner_id = GenericForeignKeyIdField(
        owner_type,
        editable=True,
        blank=True, null=True,
        verbose_name=format_lazy(u"{} {}", owner_label, _('(object)')))

    owner = GenericForeignKey(
        'owner_type', 'owner_id',
        verbose_name=owner_label)

    @classmethod
    def update_controller_field(cls, verbose_name=None, **kwargs):
        """Update attributes of the :attr:`owner` field and its underlying
        fields :attr:`owner_id` and :attr:`owner_type`.

        This can be used to make the controller optional (i.e. specify
        whether the :attr:`owner` field may be NULL). Example::

            class MyModel(Controllable):
                ....

            MyModel.update_controller_field(blank=False, null=False)

        When `verbose_name` is specified, all three fields will be
        updated, appending " (object)" and " (type)" to
        :attr:`owner_id` and :attr:`owner_type` respectively.

        """
        
        if verbose_name is not None:
            dd.update_field(cls, 'owner', verbose_name=verbose_name)
            kwargs.update(
                verbose_name=format_lazy(u"{} {}",
                    verbose_name, _('(object)')))
        dd.update_field(cls, 'owner_id', **kwargs)
        if verbose_name is not None:
            kwargs.update(
                verbose_name=format_lazy(u"{} {}",
                    verbose_name, _('(type)')))
        dd.update_field(cls, 'owner_type', **kwargs)

    def update_owned_instance(self, controllable):
        """If this (acting as a controller) is itself controlled, forward the
        call to the controller.

        """
        if self.owner:
            self.owner.update_owned_instance(controllable)
        super(Controllable, self).update_owned_instance(controllable)

    def save(self, *args, **kw):
        if settings.SITE.loading_from_dump:
            super(Controllable, self).save(*args, **kw)
        else:
            if self.owner:
                self.owner.update_owned_instance(self)
            super(Controllable, self).save(*args, **kw)
            if self.owner:
                self.owner.after_update_owned_instance(self)


    def controlled_rows(self, model, **kwargs):
        gfk = self._meta.get_field('owner')
        kwargs = gfk2lookup(gfk, self, **kwargs)
        return model.objects.filter(**kwargs)

