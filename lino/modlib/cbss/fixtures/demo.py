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
Fills in a suite of fictive IdentifyPerson requests.
"""

import os
from lino.utils import IncompleteDate
from lino.modlib.cbss.models import IdentifyPersonRequest, RequestStatus

FICTIVE_IPRS = [
    [ dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,1)), 'fictive_ipr_1.xml' ],
]

def objects():
    for kw,fn in FICTIVE_IPRS:
        ipr = IdentifyPersonRequest(
            status=RequestStatus.fictive,
            **kw
            )
        fn = os.path.join(os.path.dirname(__file__),fn)
        xml = open(fn).read()
        ipr.fill_from_string(xml)
        ipr.status = RequestStatus.fictive
        yield ipr