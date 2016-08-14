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

from django.db import models

from lino.api import dd, rt, _
from lino.modlib.users.mixins import ByUser


class Faculties(dd.Table):
    model = 'faculties.Faculty'
    # order_by = ["ref", "name"]
    detail_layout = """
    id name
    parent topic_group affinity
    FacultiesByParent CompetencesByFaculty
    """
    insert_layout = """
    # ref affinity topic_group
    name
    parent
    """


class AllFaculties(Faculties):
    label = _("Faculties (all)")
    required_roles = dd.required(dd.SiteStaff)
    column_names = 'name affinity topic_group parent *'
    order_by = ["name"]


class TopLevelFaculties(Faculties):
    label = _("Faculties (tree)")
    required_roles = dd.required(dd.SiteStaff)
    order_by = ["seqno"]
    column_names = 'seqno name children_summary parent *'
    filter = models.Q(parent__isnull=True)
    variable_row_height = True


class FacultiesByParent(Faculties):
    label = _("Child faculties")
    master_key = 'parent'
    column_names = 'seqno name affinity topic_group *'
    order_by = ["seqno"]
    # order_by = ["parent", "seqno"]
    # order_by = ["name"]
    

class Competences(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    # required_roles = dd.required(SocialStaff)
    model = 'faculties.Competence'
    column_names = 'id user faculty affinity topic *'
    order_by = ["id"]


class CompetencesByUser(Competences):
    required_roles = dd.required()
    master_key = 'user'
    column_names = 'seqno faculty affinity topic *'
    order_by = ["seqno"]


class CompetencesByFaculty(Competences):
    master_key = 'faculty'
    column_names = 'user affinity topic *'
    order_by = ["user"]


class MyCompetences(ByUser, CompetencesByUser):
    pass

if dd.is_installed('tickets'):

    class AssignableWorkersByTicket(dd.Table):
        model = 'users.User'
        # model = 'faculties.Competence'
        master = 'tickets.Ticket'
        column_names = 'username #faculties_competence_set_by_user__affinity *'
        label = _("Assignable workers")

        @classmethod
        def get_request_queryset(self, ar):
            ticket = ar.master_instance
            if ticket is None:
                return rt.models.users.User.objects.none()

            # rt.models.faculties.Competence.objects.filter(
            #     faculty=ticket.faculty)
            qs = rt.models.users.User.objects.all()
            # qs = super(
            #     AssignableWorkersByTicket, self).get_request_queryset(ar)

            if ticket.topic:
                qs = qs.filter(
                    faculties_competence_set_by_user__topic=ticket.topic)
            if ticket.faculty:
                faculties = ticket.faculty.whole_clan()
                qs = qs.filter(
                    faculties_competence_set_by_user__faculty__in=faculties)
            qs = qs.order_by('faculties_competence_set_by_user__affinity')
            return qs

