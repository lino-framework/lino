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

"""This app installs a button to "print" any table into PDf using
Pisa.

To use it, simply add the following line to your
:settings:`get_installed_apps`::

    yield 'lino.modlib.print_pisa'

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Print table using Pisa")

