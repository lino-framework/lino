# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.db import models
from django.conf import settings

from lino.api import dd, rt, _
from lino.core.roles import SiteAdmin
from lino.core import auth, layouts

class SendWelcomeMail(dd.Action):
    label = _("Welcome mail")
    if False:  # #1336
        show_in_bbar = True
        show_in_workflow = False
    else:
        show_in_bbar = False
        show_in_workflow = True
    button_text = u"\u2709"  # ✉
    required_roles = dd.login_required(SiteAdmin)
    parameters = dict(
        email=models.EmailField(_('e-mail address')),
        subject=models.CharField(_('Subject'), max_length=250),
        #body_text=dd.RichTextField(_('Body text'), format='html'),
    )
    # params_layout = dd.Panel("""email
    # subject
    # body_text""", window_size=(60, 15))

    # params_layout = dd.Panel("""
    # email
    # subject
    # welcome_email_body""", window_size=(60, 15))

    params_layout = """
    email
    subject
    """

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(SendWelcomeMail, self).action_param_defaults(
            ar, obj, **kw)
        if obj is not None:
            kw.update(email=obj.email)
        kw.update(subject=_("Welcome on {site}").format(
            site=settings.SITE.title or settings.SITE.verbose_name))
        # template = rt.get_template('users/welcome_email.eml')
        # context = dict(obj=obj, E=E, rt=rt)
        # body = template.render(**context)
        # body = E.fromstring(body)
        # kw.update(body_text=body)
        return kw

    # def get_action_permission(self, ar, obj, state):
    #     user = ar.get_user()
    #     if not obj.email:
    #         return False
    #     if not user.user_type.has_required_roles([SiteAdmin]):
    #         return False
    #     return super(
    #         SendWelcomeMail, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        sender = settings.SERVER_EMAIL
        done_for = []
        assert len(ar.selected_rows) == 1
        obj = ar.selected_rows[0]
        subject = ar.action_param_values.subject
        email = ar.action_param_values.email
        # body = ar.action_param_values.body_text
        # body = "<body>" + body + "</body>"
        email = "{} <{}>".format(obj, email)

        body = obj.get_welcome_email_body(ar)
        print(20170102, obj, email, body)
        # send_welcome_email(obj)
        rt.send_email(subject, sender, body, [email])
        done_for.append(email)

        msg = _("Welcome mail has been sent to {}.").format(
            ', '.join(done_for))
        ar.success(msg, alert=True)



class ChangePassword(dd.Action):
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

    # def get_action_permission(self, ar, obj, state):
    #     user = ar.get_user()
    #     # print("20160825", obj, user)
    #     if obj.id != user.id and \
    #        not user.user_type.has_required_roles([SiteAdmin]):
    #         return False
    #     return super(
    #         ChangePassword, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        pv = ar.action_param_values
        if pv.new1 != pv.new2:
            ar.error("New passwords didn't match!")
            return
        done_for = []
        for obj in ar.selected_rows:
            if ar.get_user().user_type.has_required_roles([SiteAdmin]) \
               or not obj.has_usable_password() \
               or obj.check_password(pv.current):
                obj.set_password(pv.new1)
                obj.full_clean()
                obj.save()
                done_for.append(str(obj))
            else:
                ar.info("Incorrect current password for %s." % obj)

        if ar.request is not None:
            auth.login(ar.request, obj)
        msg = _("New password has been set for {}.").format(
            ', '.join(done_for))
        ar.success(msg, alert=True)


class SignOut(dd.Action):
    label = _("Sign out")
    select_rows = False
    default_format = 'ajax'
    show_in_bbar = False

    def run_from_ui(self, ar, **kw):
        # print(20170921, ar.request)
        user = ar.get_user()
        auth.logout(ar.request)
        ar.success(
            _("User {} logged out.").format(user),
            goto_url=ar.renderer.front_end.build_plain_url())

from etgen.html import E
# from lino.core.fields import DisplayField, DummyField

# class SocialAuthField(DisplayField):

#     def value_from_object(self, obj, ar=None):
#         elems = []
#         elems.append(E.a("foo"))
#         return E.p(elems)

# def social_auth_field():
#     if settings.SITE.social_auth_backends:
#         return SocialAuthField()
#     return DummyField()


class SignIn(dd.Action):
    label = _("Sign in")
    select_rows = False
    parameters = dict(
        username=dd.CharField(_("Username")),
        password=dd.PasswordField(_("Password"), blank=True)
    )
    # params_layout = dd.ActionParamsLayout("""
    params_layout = dd.Panel("""
    username
    password
    """, label_align=layouts.LABEL_ALIGN_LEFT)

    http_method = "POST"

    def run_from_ui(self, ar, **kw):
        pv = ar.action_param_values
        user = auth.authenticate(
            ar.request, username=pv.username, password=pv.password)
        if user is None:
            ar.error(_("Failed to log in as {}.".format(pv.username)))
        else:
            # user.is_authenticated:
            auth.login(ar.request, user)
            ar.success(
                _("Now logged in as {}").format(user),
                close_window=True,
                goto_url=ar.renderer.front_end.build_plain_url())



class SignInWithSocialAuth(SignIn):
    # 20171207 nice as an example of a action dialog window with a
    # HtmlBox, but we don't currently use it.
    parameters = dict(
        social_auth_links=dd.HtmlBox(
            # _("Other authentications"),
            default=E.div(*settings.SITE.get_social_auth_links())),
        # social_auth_links=dd.Constant(
        #     settings.SITE.get_social_auth_links),
        # social=social_auth_field(),
        username=dd.CharField(_("Username")),
        password=dd.PasswordField(_("Password"), blank=True)
    )
    # params_layout = dd.ActionParamsLayout("""
    params_layout = dd.Panel("""
    username
    password
    social_auth_links
    """, label_align="left", window_size=(60,10))
