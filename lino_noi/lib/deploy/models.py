# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
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

"""Database models for this plugin.



"""

from __future__ import unicode_literals

from django.db import models

from lino.api import dd, rt, _

from lino_xl.lib.excerpts.mixins import Certifiable


class Milestone(Certifiable):  # mixins.Referrable):
    """A **Milestone** is a named step of evolution on a given Site.  For
    software projects we usually call them a "release" and they are
    named by a version number.

    .. attribute:: closed

       Closed milestones are hidden in most lists.

    """
    class Meta:
        app_label = 'deploy'
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')

    # project = dd.ForeignKey(
    #     'tickets.Project',
    #     related_name='milestones_by_project')
    site = dd.ForeignKey(
        'tickets.Site',
        related_name='milestones_by_site', blank=True, null=True)
    label = models.CharField(_("Label"), max_length=20, blank=True)
    expected = models.DateField(_("Expected for"), blank=True, null=True)
    reached = models.DateField(_("Reached"), blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True)
    changes_since = models.DateField(
        _("Changes since"), blank=True, null=True,
        help_text=_("In printed document include a list of "
                    "other changes since this date"))
    closed = models.BooleanField(_("Closed"), default=False)

    #~ def __unicode__(self):
        #~ return self.label

    def __unicode__(self):
        label = self.label
        if not label:
            if self.reached:
                label = self.reached.isoformat()
            else:
                label = "#{0}".format(self.id)
        return "{0}:{1}".format(self.site, label)



class Deployment(dd.Model):
    """A **deployment** is the fact that a given ticket is being fixed (or
    installed or activated) by a given milestone (to a given site).

    Deployments are visible to the user either by ticket or by milestone.

    .. attribute:: milestone

       The milestone (and site) of this deployment.

    """
    class Meta:
        app_label = 'deploy'
        verbose_name = _("Deployment")
        verbose_name_plural = _('Deployments')

    ticket = dd.ForeignKey('tickets.Ticket')
    milestone = dd.ForeignKey('deploy.Milestone')
    # remark = dd.RichTextField(_("Remark"), blank=True, format="plain")
    remark = models.CharField(_("Remark"), blank=True, max_length=250)

    @dd.chooser()
    def milestone_choices(cls, ticket):
        # if not ticket:
        #     return []
        # if ticket.site:
        #     return ticket.site.milestones_by_site.all()
        return rt.models.deploy.Milestone.objects.order_by('label')



from lino.modlib.system.choicelists import (ObservedEvent)
from lino_noi.lib.tickets.choicelists import TicketEvents, T24, combine


class TicketEventToDo(ObservedEvent):
    text = _("To do")

    def add_filter(self, qs, pv):
        if pv.start_date:
            pass
        if pv.end_date:
            qs = qs.exclude(
                deployment__milestone__reached__lte=combine(
                    pv.end_date, T24))
        return qs


TicketEvents.add_item_instance(TicketEventToDo('todo'))


    
