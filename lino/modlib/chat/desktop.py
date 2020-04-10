# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd
class ChatGroups(dd.Table):
    model = 'chat.ChatGroup'
    column_names = "created user title description *"
    required_roles = set([])
    # cell_edit = False

    detail_layout = dd.DetailLayout("""
     title ticket
     created 
     user 
     description
     ChatMembers
    """, window_size=(50, 15))

    insert_layout = dd.InsertLayout("""
    title
    description
    """)

class ChatMembers(dd.Table):
    model = "chat.ChatGroupMember"
    master_key = "group"

# from lino.core.roles import UserRole

class ChatMessages(dd.Table):
    model = 'chat.ChatMessage'
    column_names = "created user body *"
    # required_roles = [UserRole]
    # cell_edit = False

    detail_layout = dd.DetailLayout("""
     user group 
     body
    """, window_size=(50, 15))

    #parameters = ObservedDateRange(
        # user=dd.ForeignKey(
        #     settings.SITE.user_model,
        #     blank=True, null=True),
        # show_seen=dd.YesNo.field(_("Seen"), blank=True),
    #)

    #params_layout = "user start_date end_date"

    # @classmethod
    # def get_simple_parameters(cls):
    #     for p in super(Messages, cls).get_simple_parameters():
    #         yield p
    #     yield 'user'

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(ChatMessages, self).get_request_queryset(ar, **filter)
        # pv = ar.param_values
        #
        # if pv.show_seen == dd.YesNo.yes:
        #     qs = qs.filter(seen__isnull=False)
        # elif pv.show_seen == dd.YesNo.no:
        #     qs = qs.filter(seen__isnull=True)
        return qs


class ChatsByTicket(ChatMessages):
    # column_names = "chat__seen "
    display_mode = "reactive"
    reactive_elem_name = "chatter"
    master_key = "group__ticket"