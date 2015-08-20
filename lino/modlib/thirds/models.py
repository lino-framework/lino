# coding: UTF-8
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.thirds`.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino.api import dd
from lino import mixins
from lino.modlib.contacts import models as contacts
from lino.modlib.gfks.mixins import Controllable


class Third(mixins.Sequenced, contacts.PartnerDocument, Controllable):

    class Meta:
        verbose_name = _("Third Party")
        verbose_name_plural = _('Third Parties')

    remark = models.TextField(_("Remark"), blank=True, null=True)

    def summary_row(self, ar, **kw):
        #~ s = ui.href_to(self)
        return ["(", unicode(self.seqno), ") "] + list(contacts.PartnerDocument.summary_row(self, ar, **kw))

    def __unicode__(self):
        return unicode(self.seqno)
        #~ return unicode(self.get_partner())


class Thirds(dd.Table):
    model = Third
    #~ order_by = ["modified"]
    column_names = "owner_type owner_id seqno person company *"


class ThirdsByController(Thirds):
    master_key = 'owner'
    column_names = "seqno person company id *"
    slave_grid_format = 'summary'
