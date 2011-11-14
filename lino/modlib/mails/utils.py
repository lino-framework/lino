# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module deserves more documentation.

"""
import datetime

from django.utils.translation import ugettext_lazy as _

from lino.utils.choicelists import ChoiceList

class RecipientType(ChoiceList):
    """A list of possible values for the `status` field of an :class:`Event`.
    """
    label = _("Recipient Type")
    
add = RecipientType.add_item
#~ add('cc','cc',en=u"cc",de=u"Kopie an",   fr=u"cc")
#~ add('bcc','bcc',en=u"bcc",de=u"Versteckte Kopie an",   fr=u"bcc")
#~ add('to','to',en=u"to",de=u"an",   fr=u"à")
add('cc',_("cc"),alias='cc')
add('bcc',_("bcc"),alias='bcc')
add('to',_("to"),alias='to')

