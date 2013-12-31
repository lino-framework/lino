# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

.. setting:: accounts.ref_length

The max_length of reference fields

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Accounting")

    ref_length = 20

    def __init__(self, *args):
        super(Plugin, self).__init__(*args)
        if hasattr(self.site, 'accounts_ref_length'):
            v = self.site.accounts_ref_length
            raise Exception("""%s has an attribute 'accounts_ref_length'!.
You probably want to replace this by:
SITE.configure_plugins("accounts",accounts_ref_length=%r)
""" % (self.site, v))
