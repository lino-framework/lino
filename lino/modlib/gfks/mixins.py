# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from builtins import object
from django.contrib.contenttypes.models import *

from django.conf import settings

from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from lino.api import dd
from lino.core.gfks import gfk2lookup

from .fields import GenericForeignKey, GenericForeignKeyIdField


class Controllable(dd.Model):

    # Translators: will also be concatenated with '(type)' '(object)'
    owner_label = _('Controlled by')

    controller_is_optional = True

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

