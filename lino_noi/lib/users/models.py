# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Database models for :mod:`lino_noi.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_xl.lib.countries.mixins import AddressLocation
from lino.utils.addressable import Addressable
from lino_xl.lib.contacts.mixins import Contactable

from lino.modlib.users.models import *

from lino.modlib.office.roles import OfficeUser


# @python_2_unicode_compatible
class User(User, Contactable, AddressLocation, Addressable):

    """
    .. attribute:: callme_mode

        Others can call me

    """

    class Meta(User.Meta):
        app_label = 'users'
        abstract = dd.is_abstract_model(__name__, 'User')

    callme_mode = models.BooleanField(_('Call me'), default=True)

    def get_detail_action(self, ar):
        a = super(User, self).get_detail_action(ar)
        if a is not None:
            return a
        if self.callme_mode:
            return rt.actors.users.OtherUsers.detail_action
        
    @dd.htmlbox(_("About me"))
    def about_me(self, ar):
        return self.remarks
        
    # def get_default_table(self, ar):
    #     tbl = super(User, self).get_default_table(ar)
    #     return rt.actors.users.OtherUsers
    
    # def __str__(self):
    #     s = self.get_full_name()
    #     if self.callme_mode:
    #         if self.tel:
    #             s += " ({})".format(self.tel)
    #     return s


dd.update_field('users.User', 'remarks', verbose_name=_("About me"))

class UserDetail(UserDetail):
    """Layout of User Detail in Lino Welfare."""

    main = "general contact"

    general = dd.Panel("""
    box1
    remarks:40 users.AuthoritiesGiven:20
    """, label=_("General"))

    # tickets = dd.Panel("""
    # tickets.TicketsByReporter 
    # """, label=_("Tickets"))

    box1 = """
    username profile:20 partner
    open_session_on_new_ticket user_site
    language timezone
    id created modified
    """

    # cal_left = """
    # event_type access_class
    # cal.SubscriptionsByUser
    # """

    # cal = dd.Panel("""
    # cal_left:30 cal.TasksByUser:60
    # """, label=dd.plugins.cal.verbose_name,
    #                required_roles=dd.login_required(OfficeUser))

    contact = dd.Panel("""
    address_box info_box
    topics.InterestsByPartner faculties.CompetencesByUser
    """, label=_("Contact"))

    info_box = """
    email:40
    url
    phone
    gsm
    """
    address_box = """
    first_name last_name initials
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    # addr2
    """


Users.detail_layout = UserDetail()


class OtherUsers(Users):
    hide_top_toolbar = True
    use_as_default_table = False
    editable = False
    required_roles = dd.required()
    detail_layout = dd.DetailLayout("""
    first_name last_name city user_site
    phone gsm
    about_me
    """, window_size=(60, 15))

# def site_setup(site):
#     site.modules.users.Users.set_detail_layout(UserDetail())
