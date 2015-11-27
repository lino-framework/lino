# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.
"""Database models for :mod:`lino_noi.lib.faculties`.

Defines the models :class:`Broker`, :class:`Faculty` and
:class:`Competence`.
"""

import logging
from lino_noi.lib.tickets.models import *

logger = logging.getLogger(__name__)
from lino import mixins
from django.utils.translation import ugettext_lazy as _
from lino.api import dd
import decimal
from lino.modlib.users.mixins import UserAuthored

MAX_WEIGHT = decimal.Decimal('10')


class Faculty(mixins.BabelNamed):
    """A Faculty (Fachbereich) is a conceptual (not organizational)
    department of this PCSW.  Each Newcomer will be assigned to one
    and only one Faculty, based on his/her needs.

    """

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")

    # ~ body = dd.BabelTextField(_("Body"),blank=True,format='html')
    weight = models.IntegerField(
        _("Work effort"),  # Arbeitsaufwand
        default=MAX_WEIGHT,
        help_text=u"""\
Wieviel Aufwand ein Neuantrag in diesem Fachbereich allgemein verursacht
(0 = gar kein Aufwand, %d = maximaler Aufwand).""" % MAX_WEIGHT)


class Competence(UserAuthored, mixins.Sequenced):
    """
    A competence is when a given user is declared to be competent
    in a given faculty.
    """

    class Meta:
        # ~ abstract = True
        verbose_name = _("Competence")
        verbose_name_plural = _("Competences")

    faculty = models.ForeignKey('faculties.Faculty')
    weight = models.IntegerField(
        _("Work effort"),  # Arbeitsaufwand
        blank=True,
        help_text=u"""\
Wieviel Aufwand mir persönlich ein Neuantrag in diesem Fachbereich verursacht
(0 = gar kein Aufwand, %d = maximaler Aufwand).""" % MAX_WEIGHT)

    def full_clean(self, *args, **kw):
        if self.weight is None:
            self.weight = self.faculty.weight
        super(Competence, self).full_clean(*args, **kw)

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)


dd.update_field(Competence, 'user', verbose_name=_("User"))

dd.inject_field('tickets.Ticket',
                'faculty',
                models.ForeignKey("faculties.Faculty",
                                  blank=True, null=True))

from .ui import *
