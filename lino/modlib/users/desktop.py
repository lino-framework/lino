# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Desktop UI for this plugin.

Documentation is in :doc:`/specs/users` and :doc:`/dev/users`

"""

from lino.api import dd, rt, _
from lino.core import actions
from lino.core.roles import SiteAdmin

from .choicelists import UserTypes
from .actions import SendWelcomeMail

class UserDetail(dd.DetailLayout):

    box1 = """
    username profile:20 partner
    first_name last_name initials
    email language timezone
    id created modified
    """

    main = """
    box1 #MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20
    """


class UserInsertLayout(dd.InsertLayout):

    window_size = (60, 'auto')

    main = """
    username email
    first_name last_name
    partner
    language profile
    """


class Users(dd.Table):
    #~ debug_actions  = True
    model = 'users.User'
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    active_fields = 'partner'

    parameters = dict(
        profile=UserTypes.field(blank=True))

    simple_parameters = ['profile']

    #~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = 'username profile first_name last_name *'
    detail_layout = UserDetail()
    insert_layout = UserInsertLayout()

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
    required_roles = dd.login_required(SiteAdmin)
    send_welcome_email = SendWelcomeMail()

class UsersOverview(Users):

    column_names = 'username profile language'
    exclude = dict(profile='')

class MySettings(Users):
    use_as_default_table = False
    hide_top_toolbar = True
    required_roles = dd.login_required()
    default_list_action_name = 'detail'

    @classmethod
    def get_default_action(cls):
        return actions.ShowDetail()


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


