# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.davlink`.

.. autosummary::

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd


class ResetDavLink(dd.Action):
    label = _("Reset DavLink")
    js_handler = 'Lino.davlink_reset'
    readonly = True

    def attach_to_actor(self, actor, name):
        # logger.info("20140923 %r %r", actor, name)
        return super(ResetDavLink, self).attach_to_actor(actor, name)


class Toolbar(dd.Actor):
    reset_davlink = ResetDavLink()


def setup_quicklinks(self, ar, tb):
    tb.add_action('davlink.Toolbar', 'reset_davlink')  # , align="right")

