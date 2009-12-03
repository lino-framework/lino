## Copyright 2009 Luc Saffre
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



class Condition:
    pass
    
class never(Condition):
    @staticmethod
    def passes(request): return False
      
class always(Condition):        
    @staticmethod
    def passes(request): return True
      
class is_staff(Condition):        
    @staticmethod
    def passes(request):
        #print "requests.is_staff()", request.user.is_staff
        return request.user.is_staff
        
class is_authenticated(Condition):
    @staticmethod
    def passes(request):
        #print request.user, request.user.is_authenticated
        return request.user.is_authenticated()

class is_anonymous(Condition):
    @staticmethod
    def passes(request):
        return not request.user.is_authenticated()
        
        
from django.conf import settings

if settings.BYPASS_PERMS:
    is_authenticated.passes = staticmethod(always.passes)
    is_staff.passes = staticmethod(always.passes)

#~ def always(request): return True
#~ def is_staff(request): 
    #~ print "requests.is_staff()", request.user.is_staff
    #~ return request.user.is_staff
#~ def is_authenticated(request): return request.user.is_authenticated()

#~ class AND:
  #~ def __init__(self,*tests):
      #~ self.tests = tests
  #~ def test(self,*args,**kw):
      #~ for t in self.tests:
          #~ if not t(*args,**kw):
              #~ return False
      #~ return True
