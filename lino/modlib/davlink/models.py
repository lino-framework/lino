# Copyright 2008-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _

from lino.api import dd


class ResetDavLink(dd.Action):
    label = _("Reset DavLink")
    js_handler = 'Lino.davlink_reset'
    readonly = True

    def attach_to_actor(self, actor, name):
        # print ("20140923 %r %r", actor, name)
        return super(ResetDavLink, self).attach_to_actor(actor, name)


class Toolbar(dd.Actor):
    reset_davlink = ResetDavLink()


