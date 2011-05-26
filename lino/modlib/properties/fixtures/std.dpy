# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.


from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values
from lino.utils.choicelists import HowWell

#~ def objects():
    #~ ptype = Instantiator('properties.PropType').build
    
    #~ division = ptype(**babel_values('name',**dict(en="Division",fr="Division",de=u"Abteilung")))
    #~ yield division
    #~ divchoice = Instantiator('properties.PropChoice','value',type=division).build
    #~ yield divchoice('1',**babel_values('text',**dict(en="Furniture",de=u"Möbel",fr=u"Meubles")))
    #~ yield divchoice('1',**babel_values('text',**dict(en="Web hosting",de=u"Hosting",fr=u"Hosting")))
  

def objects():
    ptype = Instantiator('properties.PropType').build
    yield ptype(id=1,**babel_values('name',**dict(
        en="Present or not",
        de=u"Vorhanden oder nicht",
        fr=u"Présent ou pas",
        nl=u"Ja of niet",
        )))
    yield ptype(id=2,
        choicelist=HowWell.__name__,
        default_value=HowWell.default.value,
        **babel_values('name',**dict(
            en="Appraisal",
            de=u"Bewertung",
            fr=u"Appréciation(?)",
            nl=u"Hoe goed",
            )))
    
