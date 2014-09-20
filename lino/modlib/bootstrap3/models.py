# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
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

from django.conf import settings
# from django.db import models
# from lino.core import actions
from lino.core.tables import AbstractTable
from django.utils.translation import ugettext_lazy as _

from lino import dd, rt


class ShowAsHtml(dd.Action):
    label = _("HTML")
    help_text = _('Show this table in Bootstrap3 interface')
    icon_name = 'html'
    sort_index = -15
    select_rows = False
    default_format = 'ajax'
    preprocessor = "Lino.get_current_grid_config"

    def is_callable_from(self, caller):
        return isinstance(caller, dd.GridEdit)

    def run_from_ui(self, ar, **kw):
        url = dd.plugins.bootstrap3.renderer.get_request_url(ar)
        ar.success(open_url=url)

if settings.SITE.default_ui != 'bootstrap3':
    AbstractTable.show_as_html = ShowAsHtml()
