# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Actions for this plugin.

"""
from builtins import str
from builtins import object

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


from lino.api import dd, rt
from lino.core.roles import SiteAdmin


class SendWelcomeMail(dd.Action):
    """Send a welcome mail to this user."""
    label = _("Welcome mail")
    show_in_bbar = True
    show_in_workflow = False
    button_text = u"\u2709"  # ✉
    required_roles = dd.required(SiteAdmin)
    parameters = dict(
        email=models.EmailField(_('e-mail address')),
        verification_code=models.CharField(
            _("Verification code"), max_length=50))
    
    
    def get_action_permission(self, ar, obj, state):
        if obj == ar.get_user():
            return False
        return super(
            SendWelcomeMail, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        done_for = []
        for obj in ar.selected_rows:
            obj.send_welcome_email()
            done_for.append(str(obj))

        msg = _("Welcome mail has been sent to {}.").format(
            ', '.join(done_for))
        ar.success(msg, alert=True)



class ChangePassword(dd.Action):
    """Change the password of this user.

    .. attribute:: current

        The current password. Leave empty if the user has no password
        yet. And SiteAdmin users don't need to specify this at all.

    .. attribute:: new1

        The new password.

    .. attribute:: new2

        The new password a second time. Both passwords must match.

    """
    # button_text = u"\u205C"  # DOTTED CROSS (⁜)
    # button_text = u"\u2042"  # ASTERISM (⁂)
    button_text = u"\u2731" # 'HEAVY ASTERISK' (✱)
    # icon_name = "disk"
    label = _("Change password")
    
    parameters = dict(
        current=dd.PasswordField(_("Current password"), blank=True),
        new1=dd.PasswordField(_("New password"), blank=True),
        new2=dd.PasswordField(_("New password again"), blank=True)
    )
    params_layout = """
    current
    new1
    new2
    """

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        # print("20160825", obj, user)
        if obj != user and \
           not user.profile.has_required_roles([SiteAdmin]):
            return False
        return super(
            ChangePassword, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        
        pv = ar.action_param_values
        if pv.new1 != pv.new2:
            ar.error("New passwords didn't match!")
            return
        done_for = []
        for obj in ar.selected_rows:
            if ar.get_user().profile.has_required_roles([SiteAdmin]) \
               or not obj.has_usable_password() \
               or obj.check_password(pv.current):
                obj.set_password(pv.new1)
                obj.full_clean()
                obj.save()
                done_for.append(str(obj))
            else:
                ar.info("Incorrect current password for %s." % obj)

        msg = _("New password has been set for {}.").format(
            ', '.join(done_for))
        ar.success(msg, alert=True)


