# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import _
from lino.modlib.users.choicelists import SiteUser


class ReceptionClerk(SiteUser):
    text = _("Reception clerk")


