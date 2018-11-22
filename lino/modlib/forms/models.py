# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Rumma & Ko Ltd
"""
Database models for `lino.modlib.bootstrap3`.

.. autosummary::

"""


from django.conf import settings
from lino.core.tables import AbstractTable
from django.utils.translation import ugettext_lazy as _

from lino.api import dd


class ShowAsHtml(dd.Action):
    label = _("HTML")
    help_text = _('Show this table in Bootstrap3 interface')
    icon_name = 'html'
    sort_index = -15
    select_rows = False
    default_format = 'ajax'
    preprocessor = "Lino.get_current_grid_config"
    callable_from = 't'

    # def is_callable_from(self, caller):
    #     return isinstance(caller, dd.ShowTable)

    def run_from_ui(self, ar, **kw):
        url = dd.plugins.bootstrap3.renderer.get_request_url(ar)
        ar.success(open_url=url)

if settings.SITE.default_ui != 'lino.modlib.bootstrap3':
    AbstractTable.show_as_html = ShowAsHtml()
