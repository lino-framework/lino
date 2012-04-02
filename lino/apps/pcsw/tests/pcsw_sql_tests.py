# -*- coding: utf-8 -*-
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
This module runs a series of tests on whether Lino issues the correct SQL requests.

You can run only these tests by issuing::

  python manage.py test pcsw.SqlTest

See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_sql_tests.py`.

"Regardless of the value of the DEBUG setting in your configuration file, 
all Django tests run with DEBUG=False. This is to ensure that the observed 
output of your code matches what will be seen in a production setting."  
(https://docs.djangoproject.com/en/dev/topics/testing)

Fortunately Django gives a possibility to override this:
`Overriding settings <https://docs.djangoproject.com/en/dev/topics/testing/#overriding-settings>`_ 

[Note1] 
Because we are applying Django's `override_settings` decorator *to the whole class*, 
we need to also set :attr:`lino.utils.test.TestCase.defining_module`.
  
  
"""
import logging
logger = logging.getLogger(__name__)

import pprint

import datetime

NOW = datetime.datetime.now() 

from django.conf import settings
from django.test.utils import override_settings

from lino.utils import i2d
from lino.utils import babel
from lino.tools import resolve_model

from lino.utils.instantiator import Instantiator

def create_user(*args):
    user = Instantiator('users.User',
      'username email first_name last_name is_staff is_superuser',
      is_active=True,last_login=NOW,date_joined=NOW).build
    return user(*args)



from lino.utils.test import TestCase 

@override_settings(DEBUG=True) 
class SqlTest(TestCase):
    defining_module = __name__  # [Note1]
    
  
  
def test01(self):
    """
    Test the number of SQL queries for certain requests.
    """
    
    #~ settings.LINO.setup()
    
    from lino.modlib.users.models import User
    
    #~ user = create_user('user','user@example.com','John','Jones',False,False)
    #~ user.save()
    root = create_user('root','root@example.com','Dick','Dickens',True,True)    
    root.save()
    
    self.check_sql_queries(
      'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      'SELECT (1) AS "a" FROM "lino_siteconfig" [...]',
      'INSERT INTO "lino_siteconfig" [...]',
      'SELECT (1) AS "a" [...] WHERE "contacts_partner"."id" = 100  LIMIT 1',
      'INSERT INTO "contacts_partner" [...]',
      'SELECT (1) AS "a" FROM "users_user" WHERE "users_user"."partner_ptr_id" = 100  LIMIT 1',
      'INSERT INTO "users_user" [...]'
    )

   
    url = '/api/contacts/Companies?fmt=json&limit=30&start=0'
    response = self.client.get(url,REMOTE_USER='root')
    
    self.check_sql_queries(
      'SELECT "contacts_partner"."id", [...] WHERE "users_user"."username" = root',
      'SELECT "contacts_partner"."id", [...] ORDER BY "contacts_partner"."name" ASC LIMIT 30',
      'SELECT COUNT(*) FROM "contacts_company"',
    )
    
    #~ self.check_sql_queries(
      #~ 'SELECT "pcsw_persongroup"."id", [...] ORDER BY "pcsw_persongroup"."ref_name" ASC',
      #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      #~ 'SELECT "contacts_contact"."id", [...] WHERE "users_user"."username" = root',
      #~ 'SELECT "contacts_contact"."id", [...] ORDER BY "contacts_contact"."name" ASC LIMIT 30',
      #~ 'SELECT COUNT(*) FROM "contacts_company"',
    #~ )
    
    #~ response = self.client.get('/',REMOTE_USER='root')
    
