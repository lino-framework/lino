# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

from django.utils.translation import ugettext_lazy as _
from lino.utils.choicelists import ChoiceList


class TicketStates(ChoiceList):
    """
    The state of a ticket (new, open, closed, ...)
    """
    label = _("Ticket State")

add = TicketStates.add_item

add('10',_("New"),'new')
add('20',_("Assigned"),'assigned')
add('30',_("Closed"),'closed')