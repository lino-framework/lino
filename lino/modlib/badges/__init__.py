# Copyright 2014 Luc Saffre
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

"""This module is internally named after the notion of
`Scout badges <http://en.wikipedia.org/wiki/Scout_badge>`.

It defines two models "Badge" and "Award".  Badges represent the
different achievement levels that can be awarded.  An Award is when a
given "holder" has the right to wear a given Badge.  The date of an
Award is the day when the holder passed a test or something equivalent.

**Settings**

.. setting:: badges.holder_model

A string referring to the model which represents the badge holder in
your application.  Default value is ``'contacts.Person'``.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    """A singleton instance of will be publically available as
    ``dd.apps.badges.``"""

    verbose_name = _("Badges")

    ## settings
    holder_model = 'contacts.Person'
