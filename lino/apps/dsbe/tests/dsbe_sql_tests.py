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
This module contains "quick" tests that are 
run with only the ``std`` fixture. You can run only these tests by issuing::

  python manage.py test dsbe.SqlTest

See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_sql_tests.py`.

  Overriding settings
  See https://docs.djangoproject.com/en/dev/topics/testing/#overriding-settings
  
  "Regardless of the value of the DEBUG setting in your configuration file, all Django tests run with DEBUG=False. This is to ensure that the observed output of your code matches what will be seen in a production setting."  
  (https://docs.djangoproject.com/en/dev/topics/testing)
  
[Note1] When using Django's override_settings decorator, 
        we need to set :attr:`lino.utils.test.TestCase.defining_module`.
  
  
"""
import logging
logger = logging.getLogger(__name__)

import pprint

import datetime

NOW = datetime.datetime.now() 

from django.conf import settings
from django.db import connection, reset_queries
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
    
    def check_sql_queries(self,*expected):
        for i,x1 in enumerate(expected):
            sql = connection.queries[i]['sql'].strip()
            x2 = x1.split('[...]')
            if len(x2) == 2:
                s = x2.pop().strip()
                if not sql.endswith(s):
                    self.fail("SQL %d doesn't end with %s:---\n%s\n---" % (i,s,sql))
                    
            self.assertEqual(len(x2),1)
            s = x2[0].strip()
            if not sql.startswith(s):
                self.fail("SQL %d doesn't start with %s:---\n%s\n---" % (i,s,sql))
        if len(expected) < len(connection.queries):
            for q in connection.queries[len(expected):]:
                logger.warning("Unexpected SQL:---\n%s\n---",q['sql'])
            self.fail("Found unexpected SQL")
        reset_queries()
                    
  
  
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
      'SELECT (1) AS "a" [...] WHERE "contacts_contact"."id" = 100  LIMIT 1',
      'INSERT INTO "contacts_contact" [...]',
      'SELECT (1) AS "a" FROM "users_user" WHERE "users_user"."contact_ptr_id" = 100  LIMIT 1',
      'INSERT INTO "users_user" [...]'
    )

   
    url = '/api/contacts/Companies?fmt=json&limit=30&start=0'
    response = self.client.get(url,REMOTE_USER='root')
    
    self.check_sql_queries(
      'SELECT "dsbe_persongroup"."id", [...] ORDER BY "dsbe_persongroup"."ref_name" ASC',
      'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
      'SELECT "contacts_contact"."id", [...] WHERE "users_user"."username" = root',
    )
    
    #~ response = self.client.get('/',REMOTE_USER='root')
    
