# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

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

from lino import dd

from lino.modlib.courses.models import EnrolmentStates


class PrintAndChangeStateAction(dd.ChangeStateAction):
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        
        def ok():
            # to avoid UnboundLocalError local variable 'kw' referenced before assignment
            kw2 = obj.do_print.run_from_ui(ar,**kw)
            kw2 = super(PrintAndChangeStateAction,self).run_from_ui(ar,**kw2)
            kw2.update(refresh_all=True)
            return kw2
        msg = self.get_confirmation_message(obj,ar)
        return ar.confirm(ok, msg, _("Are you sure?"))
    
#~ class ConfirmEnrolment(PrintAndChangeStateAction):
    #~ required = dd.required(states='requested')
    #~ label = _("Confirm")
    #~ 
    #~ def get_confirmation_message(self,obj,ar):
        #~ return _("Confirm enrolment of <b>%(pupil)s</b> to <b>%(course)s</b>.") % dict(
            #~ pupil=obj.pupil,course=obj.course)        
    
class CertifyEnrolment(PrintAndChangeStateAction):
    required = dd.required(states='confirmed')
    label = _("Certify")
    #~ label = _("Award")
    #~ label = school.EnrolmentStates.award.text
    
    def get_confirmation_message(self,obj,ar):
        return _("Print certificate for <b>%(pupil)s</b>.") % dict(
            pupil=obj.pupil,course=obj.course)
    

    

class ConfirmEnrolment(dd.ChangeStateAction):
    label = _("Confirm")
    #~ icon_name = 'cancel'
    #~ required = dict(states='assigned',owner=True)
    #~ required = dict(states='published rescheduled took_place')#,owner=True)
    required = dict(states='requested')#,owner=True)
    help_text=_("Check for possible problems.")
  
    def run_from_ui(self,ar,**kw):
        #~ problems = []
        for obj in ar.selected_rows:
            msg = obj.get_confirm_veto(ar)
            if msg is None:
                obj.state = EnrolmentStates.confirmed
                obj.save()
                kw.update(refresh_all=True)
            else:
                msg = _("Cannot confirm %(pupil)s : %(message)s") % dict(pupil=obj.pupil,message=msg)
                kw.update(message=msg,alert=True)
                break
        return kw
    

    

@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None,**kw):
    
    EnrolmentStates.confirmed.add_transition(ConfirmEnrolment)
    EnrolmentStates.certified.add_transition(CertifyEnrolment)
    EnrolmentStates.cancelled.add_transition(_("Cancel"),states="confirmed")
