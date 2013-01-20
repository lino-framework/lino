# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre
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
This installs fictive root users (administrators), one for each language.
We are trying to sound realistic without actually hitting any real person.
These names are also visible in the :doc:`Lino demo sites </demos>`.

"""

import datetime
from django.conf import settings
from lino import dd
from lino.utils.instantiator import Instantiator
from lino.utils import babel

def root_user(lang,**kw):
    #~ kw.update(profile='900') # UserProfiles.admin) 
    kw.update(profile=dd.UserProfiles.admin) 
    kw.update(email='root@example.com') 
    kw.update(language=lang) 
    if lang == 'de':
        #~ kw.update(first_name="Rudi",last_name=u"Rutté")
        kw.update(first_name="Rolf",last_name=u"Rompen")
    elif lang == 'fr':
        kw.update(first_name=u"Romain",last_name=u"Raffault")
    elif lang == 'et':
        kw.update(first_name="Rando",last_name=u"Roosi")
    elif lang == 'en':
        kw.update(first_name="Robin",last_name="Rood")
    elif lang == 'nl':
        kw.update(first_name="Rik",last_name="Rozenbos")
    else:
        return None
    kw.update(username=kw.get('first_name').lower()) 
    return kw

def objects():
    User = settings.LINO.user_model
    if User is not None:
        for lang in babel.AVAILABLE_LANGUAGES:
            kw = root_user(lang)
            if kw:
                u = User(**kw)
                #~ u.set_password('1234')
                yield u
