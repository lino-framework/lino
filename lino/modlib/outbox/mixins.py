# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
from lino import dd


class RecipientTypes(dd.ChoiceList):

    """A list of possible values for the `type` field of a
    :class:`Recipient`.

    """
    verbose_name = _("Recipient Type")

add = RecipientTypes.add_item
add('to', _("to"), 'to')
add('cc', _("cc"), 'cc')
add('bcc', _("bcc"), 'bcc')
#~ add('snail',_("Snail mail"),'snail')


