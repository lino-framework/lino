# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This defines the :class:`ml.excerpts.Certifiable` model mixin.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino import dd


class Shortcut(dd.Choice):
    model_spec = None

    def __init__(self, model_spec, name, verbose_name):
        self.model_spec = model_spec
        value = model_spec + "." + name
        super(Shortcut, self).__init__(value, verbose_name, name)


class Shortcuts(dd.ChoiceList):
    verbose_name = _("Excerpt shortcut")
    verbose_name_plural = _("Excerpt shortcuts")
    item_class = Shortcut


class Certifiable(dd.Model):

    class Meta:
        abstract = True

    printed_by = dd.ForeignKey(
        'excerpts.Excerpt',
        verbose_name=_("Printed"),
        editable=False,
        related_name="%(app_label)s_%(class)s_set_as_printed",
        blank=True, null=True,
    )

    def disabled_fields(self, ar):
        if self.printed_by_id is None:
            return set()
        return self.CERTIFIED_FIELDS

    @classmethod
    def on_analyze(cls, site):
        # Contract.user.verbose_name = _("responsible (DSBE)")
        cls.CERTIFIED_FIELDS = dd.fields_list(
            cls,
            cls.get_certifiable_fields())
        super(Certifiable, cls).on_analyze(site)

    @classmethod
    def get_certifiable_fields(cls):
        return ''

    @dd.displayfield(_("Printed"))
    def printed(self, ar):
        ex = self.printed_by
        if ex is None:
            return ''
        return ar.obj2html(ex, naturaltime(ex.build_time))

    def clear_cache(self):
        obj = self.printed_by
        if obj is not None:
            self.printed_by = None
            self.full_clean()
            self.save()
            obj.delete()


