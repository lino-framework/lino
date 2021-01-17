# -*- coding: UTF-8 -*-
# Copyright 2011-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Desktop UI for this plugin.

Documentation is in :doc:`/specs/users` and :doc:`/dev/users`

"""

from datetime import datetime
from textwrap import wrap
from importlib import import_module
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.conf import settings
from django.db import models

from lino.api import dd, rt, _
from lino.core import actions
from lino.core.roles import SiteAdmin, SiteUser, UserRole
from lino.core.utils import djangoname
from lino.core.auth import SESSION_KEY

from .choicelists import UserTypes
from .actions import SendWelcomeMail, SignIn, SignInWithSocialAuth


def mywrap(t, ls=80):
    t = '\n'.join([
        ln.strip() for ln in t.splitlines() if ln.strip()])
    return '\n'.join(wrap(t, ls))


class UserDetail(dd.DetailLayout):

    box1 = """
    username user_type:20 partner
    first_name last_name initials
    email language time_zone
    id created modified
    """

    main = """
    box1 #MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20 SocialAuthsByUser:30
    """

    # main_m = """
    # username
    # user_type
    # partner
    # first_name last_name
    # initials
    # email language time_zone
    # id created modified
    # remarks
    # AuthoritiesGiven
    # """


class UserInsertLayout(dd.InsertLayout):

    window_size = (60, 'auto')

    main = """
    username email
    first_name last_name
    partner
    language user_type
    """


class Users(dd.Table):
    #~ debug_actions  = True
    model = 'users.User'
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    active_fields = 'partner'
    abstract = True
    required_roles = dd.login_required(SiteAdmin)

    parameters = dict(
        user_type=UserTypes.field(blank=True))

    simple_parameters = ['user_type']

    #~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = 'username user_type first_name last_name *'
    detail_layout = 'users.UserDetail'
    insert_layout = UserInsertLayout()
    # column_names_m = 'mobile_item *'

    @classmethod
    def render_list_item(cls, obj, ar):
        return "<p>{}</p>".format(obj.username)

    #~ @classmethod
    #~ def get_row_permission(cls,action,user,obj):
        #~ """
        #~ Only system managers may edit other users.
        #~ See also :meth:`User.disabled_fields`.
        #~ """
        #~ if not super(Users,cls).get_row_permission(action,user,obj):
            #~ return False
        #~ if user.level >= UserLevel.manager: return True
        #~ if action.readonly: return True
        #~ if user is not None and user == obj: return True
        #~ return False



class AllUsers(Users):
    send_welcome_email = SendWelcomeMail()

class UsersOverview(Users):
    required_roles = set([])
    column_names = 'username user_type language'
    exclude = dict(user_type='')
    # abstract = not settings.SITE.is_demo_site
    sign_in = SignIn()
    # if settings.SITE.social_auth_backends is None:
    #     sign_in = SignIn()
    # else:
    #     sign_in = SignInWithSocialAuth()

class MySettings(Users):
    # use_as_default_table = False
    # hide_top_toolbar = True
    required_roles = dd.login_required()
    default_list_action_name = 'detail'
    # detail_layout = 'users.UserDetail'

    @classmethod
    def get_default_action(cls):
        return actions.ShowDetail(cls.detail_layout, hide_navigator=True)


class Authorities(dd.Table):
    required_roles = dd.login_required(SiteAdmin)
    model = 'users.Authority'


class AuthoritiesGiven(Authorities):
    required_roles = dd.login_required()
    master_key = 'user'
    label = _("Authorities given")
    column_names = 'authorized'
    auto_fit_column_widths = True


class AuthoritiesTaken(Authorities):
    required_roles = dd.login_required()
    master_key = 'authorized'
    label = _("Authorities taken")
    column_names = 'user'
    auto_fit_column_widths = True

if settings.SITE.social_auth_backends:

    try:
        import social_django
    except ImportError:
        raise Exception(
            "Sites with social_auth_backends must also install PSA "
            "into their environment: "
            "$ pip install social-auth-app-django")


    class SocialAuths(dd.Table):
        label = _("Third-party authorizations")
        required_roles = dd.login_required(SiteAdmin)
        model = 'social_django.UserSocialAuth'

    class SocialAuthsByUser(SocialAuths):
        required_roles = dd.login_required(SiteUser)
        master_key = 'user'
else:

    class SocialAuthsByUser(dd.Dummy):
        pass



class UserRoles(dd.VirtualTable):
    label = _("User roles")
    required_roles = dd.login_required(SiteAdmin)

    @classmethod
    def get_data_rows(self, ar):
        user_roles = set()
        utm = settings.SITE.user_types_module
        if utm:
            m = import_module(utm)
            for k in dir(m):
                v = getattr(m, k)
                if not v is UserRole:
                    if isinstance(v, type) and issubclass(v, UserRole):
                        user_roles.add(v)
        # for ut in UserTypes.get_list_items():
        #     user_roles.remove(ut.role.__class__)
        return sorted(user_roles, key=djangoname)

    @dd.displayfield(_("Name"))
    def name(self, obj, ar):
        return djangoname(obj)

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        return mywrap(obj.__doc__ or '', 40)

    @classmethod
    def setup_columns(cls):
        def w(ut):
            def func(fld, obj, ar):
                if isinstance(ut.role, obj):
                    return "☑"
                return ""
            return func
        names = []
        for ut in UserTypes.get_list_items():
            name = "ut" + ut.value
            # vf = dd.VirtualField(
            #     models.BooleanField(str(ut.value)), w(ut))
            vf = dd.VirtualField(
                dd.DisplayField(str(ut.value)), w(ut))
            cls.add_virtual_field(name, vf)
            names.append(name+":3")
        # cls.column_names = "name:20 description:40 " + ' '.join(names)
        cls.column_names = "name:20 " + ' '.join(names)


def format_timestamp(dt):
    if dt is None:
        return ''
    return "{} {} ({})".format(
        dt.strftime(settings.SITE.date_format_strftime),
        dt.strftime(settings.SITE.time_format_strftime),
        naturaltime(dt))


class KillSession(actions.Action):
    label = _("Kill")
    custom_handler = True
    readonly = False
    show_in_bbar = False
    show_in_workflow = True

    def get_action_permission(self, ar, obj, state):
        if not super(KillSession, self).get_action_permission(ar, obj, state):
            return False
        # print("20210117", ar.request.session.session_key, obj.session_key)
        if ar.request.session.session_key == obj.session_key:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # print("20210117", ar.request.session.session_key, obj.session_key)
        assert ar.request.session.session_key != obj.session_key
        msg = _("Session {} has been deleted.").format(obj)
        obj.delete()
        kw = dict()
        kw.update(refresh_all=True)
        kw.update(message=msg)
        ar.success(**kw)


class Sessions(dd.Table):
    model = 'sessions.Session'
    label = _("User sessions")
    required_roles = dd.login_required(dd.SiteAdmin)
    # column_names = "last_request:30 ip_address:12 login_failures:5 blacklisted_since:12 username:20 last_login:30"
    column_names = "last_activity:30 last_ip_addr:12 username:12 session_key:20 expire_date workflow_buttons"
    window_size = (90, 12)
    kill_session = KillSession()

    @classmethod
    def get_data_rows(cls, ar):
        # qs = cls.model.objects.filter(expire_date__gt=timezone.now())
        qs = cls.model.objects.all()
        lst = []
        for ses in qs:
            row = cls.session_to_row(ses)
            if row is not None:
                # ses.session_key, ses.expire_date, data)
                lst.append(row)
        lst.sort(key=lambda ses:ses.last_activity)
        return lst

    @classmethod
    def session_to_row(cls, ses):
        data = ses.get_decoded()
        ses.data = data
        # user = users.User.objects.get(pk=data[SESSION_KEY])
        la = data.get('last_activity', None)
        if la is None:
            la = settings.SITE.startup_time
        else:
            la = datetime.strptime(la, "%Y-%m-%dT%H:%M:%S.%f")
        ses.last_activity = la
        user_id = data.get(SESSION_KEY, None)
        if user_id is None:
            ses.user = None
        else:
            u = rt.models.users.User.objects.get(pk=user_id)
            ses.user = u
        return ses

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        ses = cls.model.objects.get(pk=pk)
        return cls.session_to_row(ses)

    @dd.displayfield(_("session key"))
    def session_key(self, obj, ar):
        # ses = obj[2]
        return obj.session_key

    # @dd.displayfield(_("Blacklisted since"))
    # def blacklisted_since(self, obj, ar):
    #     return format_timestamp(obj.blacklisted_since)

    # @dd.displayfield(_("Login failures"))
    # def login_failures(self, obj, ar):
    #     return obj.login_failures

    @dd.displayfield(_("Username"))
    def username(self, obj, ar):
        # u = obj[1]
        if obj.user is None:
            return "(none)"
        return obj.user.username

    @dd.displayfield(_("Last activity"))
    def last_activity(self, obj, ar):
        return format_timestamp(obj.last_activity)

    @dd.displayfield(_("IP address"))
    def last_ip_addr(self, obj, ar):
        return obj.data.get('last_ip_addr') or "?.?.?.?"

    # @dd.displayfield(_("Device type"))
    # def device_type(self, obj, ar):
    #     return obj[3].get('device_type', '')

    @dd.displayfield(_("Expires"))
    def expire_date(self, obj, ar):
        return format_timestamp(obj.expire_date)


    # @dd.displayfield(_("Last login"))
    # def last_login(self, obj, ar):
    #     return format_timestamp(obj.last_login)
