# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This is Lino's Calendar module.





There is no "Calendar" field per Event
--------------------------------------

Note that the default implementation has no "Calendar" field per
Event. The `Event` model instead has a `get_calendar` method. 

You might extend Event in your plugin as follows::

    from lino.modlib.cal.models import *
    class Event(Event):

        calendar = dd.ForeignKey('cal.Calendar')

        def get_calendar(self):
            return self.calendar

But in other cases it would create unnecessary complexity to add such
a field. For example in :ref:`welfare` there is one calendar per User,
and thus the `get_calendar` method is implemented as follows::

    def get_calendar(self):
        if self.user is not None:
            return self.user.calendar

Or in :ref:`faggio` there is one calendar per Room. Thus the
`get_calendar` method is implemented as follows::

    def get_calendar(self):
        if self.room is not None:
            return self.room.calendar

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Calendar")
