## Copyright 2009-2010 Luc Saffre
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
    def passes(user): return False
      
class always(Condition):        
    @staticmethod
    def passes(user): return True
      
class is_staff(Condition):        
    @staticmethod
    def passes(user):
        return user.is_staff
        
class is_authenticated(Condition):
    @staticmethod
    def passes(user):
        return user is not None
        #~ return user.is_authenticated()

class is_anonymous(Condition):
    @staticmethod
    def passes(user):
        return user is None
        #~ return not user.is_authenticated()
        
        
#~ from django.conf import settings

#~ if settings.BYPASS_PERMS:
    #~ is_authenticated = always
    #~ is_staff = always
