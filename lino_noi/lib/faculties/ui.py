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

from __future__ import unicode_literals

from lino_noi.lib.tickets.ui import *
from lino.api import dd, _
from lino.modlib.users.mixins import ByUser


# class TicketDetail(TicketDetail):

#     # Replace waiting_for by faculties
#     general1 = """
#     summary:40 id:6 reporter:12
#     site product project private
#     workflow_buttons:30 assigned_to:20 faculty:20
#     """

# Tickets.detail_layout = TicketDetail()

# def site_setup(site):
#     site.modules.tickets.Tickets.set_detail_layout(TicketDetail())


class UnassignedTickets(Tickets):
    column_names = "summary project reporter *"
    label = _("Unassigned Tickets")

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.filter(assigned_to=None)


class Faculties(dd.Table):
    model = 'faculties.Faculty'
    column_names = 'ref name affinity product_cat *'
    order_by = ["ref", "name"]
    detail_layout = """
    id ref affinity product_cat
    name
    FacultiesByParent CompetencesByFaculty
    """
    insert_layout = """
    ref affinity product_cat
    name
    """


class FacultiesByParent(Faculties):
    master_key = 'parent'
    column_names = 'ref name affinity product_cat *'
    order_by = ["ref"]
    

class Competences(dd.Table):
    # required_roles = dd.required(SocialStaff)
    model = 'faculties.Competence'
    column_names = 'id user faculty affinity product *'
    order_by = ["id"]


class CompetencesByUser(Competences):
    required_roles = dd.required()
    master_key = 'user'
    column_names = 'seqno faculty affinity product *'
    order_by = ["seqno"]


class CompetencesByFaculty(Competences):
    master_key = 'faculty'
    column_names = 'user affinity product *'
    order_by = ["user"]


class MyCompetences(ByUser, CompetencesByUser):
    pass


class AssignableWorkersByTicket(dd.Table):
    model = 'faculties.Competence'
    master = 'tickets.Ticket'
    column_names = 'user affinity *'
    label = _("Assignable workers")

    @classmethod
    def get_request_queryset(self, ar):
        ticket = ar.master_instance
        if ticket is None:
            return rt.modules.tickets.Ticket.objects.none()
        
        # TODO: build a list of courses, then show events by course
        qs = super(
            AssignableWorkersByTicket, self).get_request_queryset(ar)

        if ticket.product:
            qs = qs.filter(product=ticket.product)
        if ticket.faculty:
            faculties = ticket.faculty.whole_clan()
            qs = qs.filter(faculty__in=faculties)
        return qs

