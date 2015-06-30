# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

"""
Workflows for the :mod:`lino.modlib.courses` app.
"""


import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode

from lino.api import dd, rt

from lino.modlib.courses.models import EnrolmentStates
from lino.modlib.courses.models import CourseStates


class PrintAndChangeStateAction(dd.ChangeStateAction):

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar2):
            obj.do_print.run_from_ui(ar2, **kw)
            super(PrintAndChangeStateAction, self).run_from_ui(ar2)
            ar2.set_response(refresh_all=True)

        msg = self.get_confirmation_message(obj, ar)
        ar.confirm(ok, msg, _("Are you sure?"))

#~ class ConfirmEnrolment(PrintAndChangeStateAction):
    #~ required = dd.required(states='requested')
    #~ label = _("Confirm")
    #~
    #~ def get_confirmation_message(self,obj,ar):
        #~ return _("Confirm enrolment of <b>%(pupil)s</b> to <b>%(course)s</b>.") % dict(
            #~ pupil=obj.pupil,course=obj.course)


class CertifyEnrolment(PrintAndChangeStateAction):
    required_states = 'confirmed'
    label = _("Certify")
    #~ label = _("Award")
    #~ label = school.EnrolmentStates.award.text

    def get_confirmation_message(self, obj, ar):
        return _("Print certificate for <b>%(pupil)s</b>.") % dict(
            pupil=obj.pupil, course=obj.course)


class ConfirmEnrolment(dd.ChangeStateAction):
    label = _("Confirm")
    #~ icon_name = 'cancel'
    #~ required = dict(states='assigned',owner=True)
    # ~ required = dict(states='published rescheduled took_place')#,owner=True)
    required_states = 'requested'  # ,owner=True)
    help_text = _("Check for possible problems.")

    def run_from_ui(self, ar, **kw):
        #~ problems = []
        for obj in ar.selected_rows:
            msg = obj.get_confirm_veto(ar)
            if msg is None:
                obj.state = EnrolmentStates.confirmed
                obj.save()
                ar.set_response(refresh_all=True)
            else:
                msg = _("Cannot confirm %(pupil)s : %(message)s") % dict(
                    pupil=obj.pupil, message=msg)
                ar.set_response(message=msg, alert=True)
                break


@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None, **kw):

    EnrolmentStates.confirmed.add_transition(ConfirmEnrolment)
    # EnrolmentStates.certified.add_transition(CertifyEnrolment)
    EnrolmentStates.cancelled.add_transition(
        # _("Cancel"),
        required_states="confirmed requested")
    EnrolmentStates.requested.add_transition(
        # _("Reset"),
        required_states="confirmed cancelled")

    CourseStates.registered.add_transition(
        # _("Register"),
        required_states="draft")
    # CourseStates.started.add_transition(states="registered")
    # CourseStates.ended.add_transition(states="started")
    # CourseStates.cancelled.add_transition(
    #     # _("Cancel"),
    #     states="draft registered")
    CourseStates.draft.add_transition(
        # _("Reset"),
        required_states="registered")
