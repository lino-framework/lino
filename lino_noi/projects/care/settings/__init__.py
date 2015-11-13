# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

"""

.. autosummary::
   :toctree:

   demo
   doctests
   www
   memory



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino_noi.projects.team.settings import *


class Site(Site):

    verbose_name = "Lino Noi (Care)"

    demo_fixtures = ['std', 'demo', 'demo2']
    user_profiles_module = 'lino_noi.projects.care.roles'


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
