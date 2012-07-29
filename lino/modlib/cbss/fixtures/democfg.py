# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
Fills CBSS demo settings to SiteConfig
"""

from django.conf import settings
from lino import dd

def objects():
  
    Sector = dd.resolve_model('cbss.Sector')
    sc = settings.LINO.site_config
    sc.sector = Sector.objects.get(code=17,subcode=1)
    sc.cbss_org_unit = '0123456789'
    sc.ssdn_email = 'info@example.com'
    sc.ssdn_user_id = '00901234567'
    sc.cbss_http_username = 'E0123456789'
    sc.cbss_http_password = 'p1234567890123456789012345678'
    yield sc
