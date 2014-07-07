# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino-Cosi project.
# Lino-Cosi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Cosi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Cosi; if not, see <http://www.gnu.org/licenses/>.

import os

execfile(os.path.join(os.path.dirname(__file__), 'project_info.py'))
__version__ = SETUP_INFO['version']

intersphinx_url = "http://noi.lino-framework.org"
srcref_url = 'https://github.com/lsaffre/lino-noi/blob/master/%s'
