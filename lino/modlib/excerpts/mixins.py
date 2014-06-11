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

"""
This defines the :class:`ml.excerpts.Certifiable` model mixin.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd


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
    def on_analyze(cls, lino):
        # Contract.user.verbose_name = _("responsible (DSBE)")
        cls.CERTIFIED_FIELDS = dd.fields_list(
            cls,
            cls.get_certifiable_fields())
        super(Certifiable, cls).on_analyze(lino)

    @classmethod
    def get_certifiable_fields(cls):
        return ''

    @dd.displayfield(_("Printed"))
    def printed(self, ar):
        if self.printed_by_id is None:
            return ''
        return ar.obj2html(self.printed_by)

    def clear_cache(self):
        obj = self.printed_by
        if obj is not None:
            self.printed_by = None
            self.full_clean()
            self.save()
            obj.delete()

